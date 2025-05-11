import os
from datetime import datetime
import openai
from dotenv import load_dotenv
load_dotenv()
# Postavi tvoj OpenAI API ključ ovde
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY"

results_dir = "results"
output_dir = "reports"
os.makedirs(output_dir, exist_ok=True)
def classify_severity(output_text):
    if "remote code execution" in output_text.lower() or "root" in output_text.lower():
        return "Critical"
    elif "sql injection" in output_text.lower():
        return "High"
    elif "xss" in output_text.lower() or "open redirect" in output_text.lower():
        return "Medium"
    else:
        return "Low"

def summarize_vuln(content):
    prompt = f"""Analiziraj sledeći sigurnosni rezultat i napiši sažetak ranjivosti:
{content}

Vrati kratak opis ranjivosti, potencijalni rizik i preporuku za otklanjanje.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": prompt }],
            temperature=0.4,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"[GREŠKA] {str(e)}"

def extract_text(path):
    with open(path, "r") as f:
        lines = f.readlines()
    start = False
    content = ""
    for line in lines:
        if line.strip().lower() == "[rezultat]":
            start = True
            continue
        elif line.strip().lower().startswith("[status]"):
            break
        if start:
            content += line
    return content.strip()

def main():
    files = [f for f in os.listdir(results_dir) if f.endswith(".txt")]
    if not files:
        print("Nema fajlova za analizu u 'results/'.")
        return

    for fname in files:
        fpath = os.path.join(results_dir, fname)
        result_text = extract_text(fpath)
        if not result_text:
            print(f"[!] Preskačem {fname} — nema sadržaja u [Rezultat] sekciji.")
            continue
        print(f"[*] Analiziram {fname}...")
        summary = summarize_vuln(result_text)
        outname = fname.replace(".txt", "_ai_summary.md")
        outpath = os.path.join(output_dir, outname)
        with open(outpath, "w") as out:
            out.write(f"# AI Sažetak za {fname}\n\n")
            out.write(summary)
        print(f"[+] Sažetak snimljen u {outpath}")

if __name__ == "__main__":
    main()

