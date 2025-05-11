import requests
import json
import time
from openai import OpenAI
from core.fuzz_headers import fuzz_headers
from core.fuzz_param_splitter import fuzz_param_split
from core.fuzz_http_methods import fuzz_methods
from core.fuzz_json_body import fuzz_json
from core.agent_x_executor import run_and_log
client = OpenAI()

def agent_x(url):
    print("\n[ShadowAgentX] Izaberi režim:")
    print("1. Interaktivni (prikazuje korake)")
    print("2. Stealth (automatski izvodi bez pitanja)")
    mode = input("> ").strip()

    print(f"\n[+] Analiziram metu: {url}")
    try:
        r = requests.get(url, timeout=5)
        content = r.text[:1000]
    except Exception as e:
        print(f"[x] Ne mogu da dohvatim metu: {e}")
        return

    prompt = f"""
URL: {url}
Response: {content}

Na osnovu ovog odgovora, izaberi:
- koji fuzz modul da se koristi (headers, params, methods, json)
- koji payload (ili neka bude "AI generated")
- kratko objašnjenje zašto

Format odgovora:
{{
  "module": "headers",
  "payload": "<script>alert(1)</script>",
  "reason": "Odgovor sadrži HTML refleksiju i može se testirati XSS-om"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        ai_reply = json.loads(response.choices[0].message.content.strip())
        module = ai_reply["module"].lower()
        payload = ai_reply["payload"]
        reason = ai_reply["reason"]

        print(f"\n[AI] Modul: {module.upper()} | Payload: {payload}")
        print(f"     → {reason}")

        if mode == "1":
            potvrda = input("\n[?] Želiš da pokrenem test? (y/n): ").strip().lower()
            if potvrda != "y":
                print("[!] Test otkazan.")
                return

        print(f"\n[+] Pokrećem {module.upper()} fuzz sa payloadom...")
        time.sleep(1)


        run_and_log(url, module, payload, reason)
        else:
            print("[x] Nepoznat modul iz AI odgovora.")

    except Exception as e:
        print(f"[x] Ne mogu da parsiram AI odgovor: {e}")
