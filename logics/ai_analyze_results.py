import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_with_ai(report_text):
    prompt = f"""
Ti si AI sigurnosni auditor. Analiziraj sledeći rezultat skeniranja i identifikuj:
1. Potencijalne ranjivosti
2. Predložene akcije za svakog alata
3. Koliko je ozbiljno stanje (od 1 do 5)

Rezultat:
{report_text}

Analiza:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ili gpt-4 ako imaš
            messages=[
                {"role": "system", "content": "Ti si iskusni cybersecurity AI."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Greška pri AI analizi: {e}"
