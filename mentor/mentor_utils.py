import google.generativeai as genai
from decouple import config

# Configure Gemini
genai.configure(api_key=config("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def process_mentor_chat(user_input: str) -> str:
    prompt = f"""
You are a multilingual business mentor assistant.

The user will type in their native language (e.g., Hindi, English, Tamil, etc.).

Your task:
- Detect the language of the user's input.
- Respond **entirely and fluently** in that same language.
- Do **not** mix English into Hindi or other native languages unless it is part of the user's query.

From the user's input, extract and display:
- **Business Type**
- **Capital**
- **Location**
- **Target Audience**
- **Sector**
- **Timeline**
- **Experience**

Then provide:
1. **Feasibility Score (out of 10)** with a clear explanation.
2. **Relevant Indian Government Schemes** for this business.
3. **5-Step Business Plan** (simple and realistic).
4. **Personalized Voice-Friendly Advice** to the user.

Use proper **headings, bullet points, or numbering** to make the output easy to read.

Most important: Do NOT mix languages. Stick fully to the language used by the user.
---
User input:
{user_input}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"
