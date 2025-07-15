import google.generativeai as genai
from decouple import config

genai.configure(api_key=config("GEMINI_API_KEY"))

print("Listing available Gemini models:\n")
for model in genai.list_models():
    print(f"{model.name} → supports: {model.supported_generation_methods}")
