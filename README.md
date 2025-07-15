# Sankalp‑Setu: AI Mentor & NGO Matcher

## Overview
Sankalp‑Setu includes two AI‑powered modules integrated into a Django backend:
1. **AI Mentor** – a multilingual ChatGPT‑based mentor.
2. **NGO Matcher** – a cosine‑similarity–based NGO matchmaker.

Both modules support input/output in any language.

---

## Features
- **Multilingual Input**: Detects user's language, processes via English GPT model, and returns answers in original language.
- **AI Mentor**: Provides guidance, Q&A, and advice for NGO-related topics.
- **NGO Matcher**: Matches user interests to NGO profiles using cosine similarity on TF‑IDF vectors.

---

## Screenshots

### AI Mentor
- **User Input (in Hindi)**  
  ![User input example](images/mentor_input.png)
- **Bot Response (in Hindi)**  
  ![Bot response example](images/mentor_output.png)

### NGO Matcher
- **User Interest (in Spanish)**  
  ![Matcher input example](images/matcher_input.png)
- **Resulting Matches**  
  ![Matcher output example](images/matcher_output.png)

---

## Setup & Isolation Instructions

### 1. Clone Repo
```bash
git clone https://github.com/Lalwaniamisha789/Sankalp-Setu.git
cd Sankalp-Setu
```

### 2. Create Virtualenv & Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Django Server
```bash
python manage.py migrate
python manage.py runserver
```
### 4. Access the matcher and mentor frontends:
   - Matcher: http://localhost:8000/matcher/frontend/
   - Mentor: http://localhost:8000/mentor/frontend/

## Tech Stack 
### 1. LLMs: OpenAI ChatGPT API
### 2. Embeddings: sentence-transformers (MiniLM-L6-v2)
### 3. Similarity: scikit-learn (cosine)
### 4. Translation: deep-translator, langdetect
### 5.Backend: Django + Django REST Framework
Data: JSON (25+ NGO entries)

## License
This project is licensed under the MIT License. See LICENSE for details.

## Contributor 
Made with by 🩷🩷 Amisha Lalwani 🩷🩷.
