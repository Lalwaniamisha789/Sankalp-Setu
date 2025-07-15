import google.generativeai as genai
from decouple import config

# Configure Gemini with your API key
genai.configure(api_key=config("GEMINI_API_KEY"))

# ✅ Use a stable, supported model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def process_mentor_chat(user_input: str) -> str:
    prompt = f"""
You are a multilingual business mentor assistant. The user will type in their native language (Hindi, English, Tamil, etc.).

Respond ONLY in the language used in the user's query.

Instructions:
1. Extract the following fields from the business idea:
   - BUSINESS_TYPE, CAPITAL, LOCATION, TARGET, SECTOR, TIMELINE, EXPERIENCE

2. Then provide:
   - Feasibility score (out of 10) with reason
   - Relevant Indian government scheme info
   - A simple 5-step business plan
   - Personalized voice-friendly advice

Use the **same language as input** for the entire response.
Structure the output using bullet points or headings clearly.

User input: {user_input}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"
