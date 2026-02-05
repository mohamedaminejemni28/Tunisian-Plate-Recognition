# Tunisian-Plate-Recognition
# SmartALPR: Tunisian License Plate Recognition


<img width="1914" height="799" alt="image" src="https://github.com/user-attachments/assets/891d3e46-9613-4e99-9485-edfc11c8a55b" />


**SmartALPR** is an advanced AI project . It combines **Computer Vision** and **Generative IA (RAG/LLM)** to create a local solution specifically adapted to the unique formats of Tunisian license plates.
<img width="1911" height="771" alt="image" src="https://github.com/user-attachments/assets/36af940a-fddb-4544-be13-ef43b8d6e7fb" />

---

## 📋 Project Overview

The system is designed to handle the specificities of the Tunisian context that imported systems often struggle with, such as Arabic script and varied plate categories. It operates through a three-module pipeline:

### 1. Vision & Recognition (Computer Vision)

* 
**Vehicle Detection:** Identifying vehicles in images or video streams.


* 
**Plate Localization:** Precise segmentation of plates under real-world conditions (rain, low light, varying angles).


* 
**OCR & Extraction:** Extracting text and identifying background colors.


* 
**Compliance Check:** Verifying the format against official Tunisian rules and a mock database.



### 2. Contextual Verification (RAG & LLM)

* 
**Regulatory Analysis:** Uses **Retrieval-Augmented Generation (RAG)** to index Tunisian traffic laws and ATTT (Agence Technique des Transports Terrestres) documents.


* 
**Automated Reporting:** Generates natural language explanations for anomalies (e.g., missing "L" stickers on rental cars or incorrect colors).


* 
**AI Chatbot:** An interactive interface to query the system about detected non-conformities.



### 3. Deployment & Integration

* 
**Backend:** Powered by **FastAPI** for modular communication between Vision and LLM modules.


* 
**Frontend:** A user interface for video uploads, real-time status display, and report consultation.


* 
**Database:** Centralized storage for registration records and analysis results.



---

## 🚗 Supported Plate Formats

The system recognizes four main categories of Tunisian plates:

* 
**Ordinary:** White digits on black background (Format: `123 تونس 4567`).


* 
**Rental (Location):** Black background with a mandatory green "L" sticker.


* 
**Government/Ministries:** Red digits on white background.


* 
**Special/Temporary:** RS series (white on black background).



---

## 📊 Evaluation Metrics

To ensure high performance, the project is measured using:

* 
**Vision:** mAP@[.5:.95], Recall, Precision, and Accuracy.


* 
**RAG/LLM:** nDCG@k (retrieval relevance) and Answer Accuracy.



---





---

> 
> **Note:** This project utilizes datasets such as Ninja (709 images) and CCPD (396 images) for training and validation.
