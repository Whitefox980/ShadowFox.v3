import os
import json
from openai import OpenAI

def suggest_exploit(output):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant..."},
            {"role": "user", "content": output}
        ]
    )
    return response.choices[0].message.content.strip()
# Pokušaj da pročita OPENAI_API_KEY iz config fajla
def load_api_key():
    try:
        with open("config.json") as f:
            return json.load(f).get("OPENAI_API_KEY")
    except Exception:
        return os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=load_api_key())



def suggest_fix(output):
    prompt = f"""Na osnovu ovog skena, predloži kako developer može da zakrpi ranjivost:\n{output}"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()

def classify_severity(output_text):
    text = output_text.lower()
    if any(x in text for x in ["remote code execution", "rce", "root", "system("]):
        return "Critical"
    elif "sql" in text and "error" in text:
        return "High"
    elif "xss" in text or "script" in text:
        return "Medium"
    elif "open redirect" in text or "302" in text:
        return "Medium"
    elif "info" in text or "directory listing" in text:
        return "Low"
    else:
        return "Unknown"
