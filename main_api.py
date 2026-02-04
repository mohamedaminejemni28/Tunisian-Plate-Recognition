import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form
from typing import Optional
from modules.vision import analyze_image
from modules.database import check_compliance
from modules.brain_rag import  brain_rag

app = FastAPI(title="SmartALPR Tunisia - Système Intégré")

@app.post("/process")
async def process_all(
    file: Optional[UploadFile] = File(None),
    question: Optional[str] = Form(None) 
):
    # --- CAS 1 : Traitement de l'image (Prioritaire) ---
    if file:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            vision_data = analyze_image(temp_path)
            if not vision_data:
                return {"error": "Aucune plaque détectée."}

            ocr_text = vision_data.get("text", "")
            detected_color = vision_data.get("color", "Inconnue")
            
            # Vérification base de données
            status, db_info = check_compliance(ocr_text)

            # Rapport légal via brain_rag (RAG 1)
            legal_report = brain_rag.generate_explanation(ocr_text, detected_color, status)

            return {
                "plate_number": ocr_text,
                "detected_color": detected_color,
                "compliance_status": status,
                "registry_data": db_info,
                "legal_analysis": legal_report
            }
        except Exception as e:
            return {"error": f"Erreur traitement image : {str(e)}"}
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # --- CAS 2 : Question textuelle seule (Chatbot) ---
    if question:
        try:
            # Utilisation de brain_rag2 pour les questions générales
            answer = brain_rag.rag_chain.invoke(question)
            return {"legal_analysis": answer}
        except Exception as e:
            return {"error": f"Erreur RAG : {str(e)}"}

    # --- CAS 3 : Aucun input ---
    return {"error": "Veuillez envoyer une image ou une question."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)