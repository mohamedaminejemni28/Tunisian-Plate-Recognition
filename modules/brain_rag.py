import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Configuration propre des chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# VECTOR_DB_DIR doit pointer vers le dossier contenant les fichiers .faiss et .pkl
VECTOR_DB_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "data"))
os.environ["OPENAI_API_KEY"] = "AIzaSyBLh0iapHuY3wxoob6_Vp5we4vZjzugO8Y"



from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyBloMo8cPmf3neMQ-v4JLlB-7pLXzxkniQ"



class BrainRAG:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # CORRECTION ICI : On vérifie si index.faiss existe DIRECTEMENT dans VECTOR_DB_DIR
        faiss_file = os.path.join(VECTOR_DB_DIR, "index.faiss")
        
        if os.path.exists(faiss_file):
            self.vector_db = FAISS.load_local(
                VECTOR_DB_DIR, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 3})
            print(" Base vectorielle FAISS chargée avec succès.")
        else:
            print(f" ERREUR : index.faiss introuvable dans {VECTOR_DB_DIR}")
            self.vector_db = None

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        self.llm_gemini = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest",
    temperature=0.0,
    max_retries=3
)


        # Prompt enrichi selon les spécifications du projet [cite: 59, 60]
        self.system_prompt = """
        Tu es un expert du Code de la Route Tunisien et de l'ATTT. 
        Utilise les segments de contexte fournis pour expliquer les anomalies de plaques.
        Si une plaque est non conforme, cite la source (ex: Article 82 ou Règlement ATTT).

        CONTEXTE RÉGLEMENTAIRE:
        {context}

        QUESTION/ANOMALIE:
        {question}
        """
        self.prompt_template = ChatPromptTemplate.from_template(self.system_prompt)

        if self.vector_db:
            self.rag_chain = (
                {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
                | self.prompt_template
                | self.llm_gemini
                | StrOutputParser()
            )

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def generate_explanation(self, ocr_text, color, status):
        if not self.vector_db: return "Base de données juridique indisponible."
        query = f"Plaque: {ocr_text}, Couleur fond: {color}, Verdict initial: {status}."
        return self.rag_chain.invoke(query)






if __name__ == "__main__":
    brain_rag = BrainRAG()


    # 2. Tester une question directe via la chaîne interne (pour voir si le retriever fonctionne)
    print("\n--- TEST 1 : Recherche juridique directe ---")
    try:
        question_directe = "Quelles sont les règles pour les plaques de couleur rouge en Tunisie ?"
        reponse_directe = brain_rag.rag_chain.invoke(question_directe)
        print(f"Réponse du LLM :\n{reponse_directe}")
    except Exception as e:
        print(f"Erreur lors du test direct : {e}")

    from google.generativeai import list_models

    for m in list_models():
        print(m.name)


