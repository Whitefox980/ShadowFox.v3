import sys
import os
sys.path.append(os.path.abspath("core/ext_libs"))

from dotenv import load_dotenv
load_dotenv()

import openai

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def collect_full_data():
    payloads = []
    severities = []
    strategies = []
    logs = []

    for fname in os.listdir("reports"):
        if not fname.endswith(".pdf"):
            continue
        try:
            with open(os.path.join("reports", fname), "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "".join([p.extract_text() or "" for p in reader.pages])
                payload_match = re.search(r"Payload:\s(.+)", text)
                severity = re.search(r"SEVERITY:\s(.+)", text)
                strategy = re.search(r"Strategy Used:\s(.+)", text)

                payloads.append(payload_match.group(1) if payload_match else "")
                severities.append(severity.group(1) if severity else "Unknown")
                strategies.append(strategy.group(1) if strategy else "Unknown")

        except:
            continue

    if os.path.exists("logs/agent_log.jsonl"):
        with open("logs/agent_log.jsonl", "r") as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    continue

    return {
        "payloads": payloads[-50:],
        "severities": severities[-50:],
        "strategies": strategies[-50:],
        "logs": logs[-50:]
    }

def black_shadow_think():
    data = collect_full_data()

    prompt = f"""
Ti si Black Shadow Advisor – tajni strateški AI koji analizira prethodne AI bezbednosne izveštaje i logove, sa zadatkom da predloži:

1. Šta sledeće treba razviti u alatu ShadowFox kako bi nadmašio sve javne sigurnosne alate
2. Koje skriveno oružje treba dodati (skripte, bypass, AI kombinacije...)
3. Koji AI mehanizmi mogu da ubrzaju i osnaže ofanzivu
4. Kako koristiti postojeće slabosti sistema za prednost

Podaci:
{json.dumps(data, indent=2)}

Vrati 5-10 jasnih i naprednih predloga bez cenzure.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    print("\n[Black Shadow Advisor – STRATEŠKA VIZIJA]:\n")
    print(response.choices[0].message.content.strip())
