import json
import os
from django.conf import settings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator
from langdetect import detect

# Load NGO data from JSON
json_path = os.path.join(settings.BASE_DIR, 'matcher', 'women_business_ngos_50.json')
with open(json_path, "r", encoding="utf-8") as f:
    ngos = json.load(f)

# Load SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Preprocess and encode all NGO vectors once
ngo_descs = [f"{ngo.get('services', '')} {ngo.get('description', '')}" for ngo in ngos]
ngo_vecs = model.encode(ngo_descs)

# Matching function
def match_ngo(user_input, top_k=5):
    try:
        lang = detect(user_input)
    except:
        lang = "en"

    try:
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)
    except:
        return ["Translation failed."]

    user_vec = model.encode([translated_input])
    sims = cosine_similarity([user_vec[0]], ngo_vecs)[0]
    matches = sorted(zip(sims, ngos), key=lambda x: x[0], reverse=True)[:top_k]

    result = []
    for sim, ngo in matches:
        try:
            translated_services = GoogleTranslator(source='en', target=lang).translate(ngo.get("services", ""))
        except Exception as e:
            print("Translation error (services):", e)
            translated_services = ngo.get("services", "[Translation failed]")

        try:
            translated_desc = GoogleTranslator(source='en', target=lang).translate(ngo.get("description", ""))
        except Exception as e:
            print("Translation error (desc):", e)
            translated_desc = ngo.get("description", "[Translation failed]")

        result.append({
            "name": ngo.get("name", "NGO"),
            "location": ngo.get("location", ""),
            "website": ngo.get("website", "N/A"),
            "services": translated_services,
            "description": translated_desc,
            "similarity": float(round(sim, 2))
        })

    return result