import json
import os
import requests
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator
from langdetect import detect
from decouple import config

# ✅ Hugging Face setup
HF_TOKEN = config("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/intfloat/multilingual-e5-large"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# ✅ Define embedding function FIRST
def get_embedding(text):
    prompt = f"query: {text}"  # Required for BGE and E5 models
    payload = {
        "inputs": [prompt],
        "options": {"wait_for_model": True}
    }
    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]
    else:
        print(f"HuggingFace error ({response.status_code}):", response.text)
        return None


# ✅ Load NGO data
json_path = os.path.join(settings.BASE_DIR, 'matcher', 'women_business_ngos_50.json')
with open(json_path, "r", encoding="utf-8") as f:
    ngos = json.load(f)

# ✅ Try cached embeddings
embedding_cache_path = os.path.join(settings.BASE_DIR, 'matcher', 'cached_ngo_embeddings.json')

if os.path.exists(embedding_cache_path):
    with open(embedding_cache_path, "r", encoding="utf-8") as f:
        ngo_vecs = json.load(f)
else:
    ngo_descs = [f"{ngo.get('services', '')} {ngo.get('description', '')}" for ngo in ngos]
    ngo_vecs = []

    for i, text in enumerate(ngo_descs):
        vec = get_embedding(text)
        if vec:
            ngo_vecs.append(vec)
        else:
            print(f"Failed to get embedding for NGO {i}")
            ngo_vecs.append([0.0] * 384)  # Fill with zero vector to maintain alignment

    # Save to cache
    with open(embedding_cache_path, "w", encoding="utf-8") as f:
        json.dump(ngo_vecs, f)

# ✅ Matching function
def match_ngo(user_input, top_k=5):
    try:
        lang = detect(user_input)
    except:
        lang = "en"

    try:
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)
    except:
        return [{"error": "Translation failed."}]

    user_vec = get_embedding(translated_input)
    if user_vec is None:
        return [{"error": "Embedding failed for user input."}]

    sims = cosine_similarity([user_vec], ngo_vecs)[0]
    matches = sorted(zip(sims, ngos), key=lambda x: x[0], reverse=True)[:top_k]

    result = []
    for sim, ngo in matches:
        try:
            translated_services = GoogleTranslator(source='en', target=lang).translate(ngo.get("services", ""))
        except Exception as e:
            print("Translation error (services):", e)
            translated_services = "[Translation failed]"

        try:
            translated_desc = GoogleTranslator(source='en', target=lang).translate(ngo.get("description", ""))
        except Exception as e:
            print("Translation error (desc):", e)
            translated_desc = "[Translation failed]"

        result.append({
            "name": ngo.get("name", "NGO"),
            "location": ngo.get("location", ""),
            "website": ngo.get("website", "N/A"),
            "services": translated_services,
            "description": translated_desc,
            "similarity": float(round(sim, 2))
        })

    return result
