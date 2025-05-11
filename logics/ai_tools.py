import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

DEFAULT_MODEL = "gpt-4-0125-preview"  # Možeš ovde zameniti u "gpt-3.5-turbo" ako hoćeš test

def suggest_exploit(output, model=DEFAULT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert. Suggest a possible exploit based on the scan output."},
                {"role": "user", "content": f"Scan Output:\n{output}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[AI GREŠKA] {str(e)}"

def suggest_fix(output, model=DEFAULT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a security advisor. Suggest a mitigation for this vulnerability."},
                {"role": "user", "content": f"Vulnerability:\n{output}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[AI GREŠKA] {str(e)}"

def classify_severity(output, model=DEFAULT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Classify the severity of this vulnerability as: Low, Medium, High, or Critical."},
                {"role": "user", "content": f"Vulnerability:\n{output}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[AI GREŠKA] {str(e)}"
