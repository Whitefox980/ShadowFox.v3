from logics.ai_tools import suggest_exploit, suggest_fix, classify_severity
from logics.generate_pdf import save_ai_report_to_pdf

def ai_trigger_if_needed(payload, response_text, url, reflected=False, size_diff=0):
    if not reflected and abs(size_diff) < 30:
        return

    print("   [AI] Uslov zadovoljen, pokrećem analizu...")

    exploit = suggest_exploit(response_text)
    fix = suggest_fix(response_text)
    severity = classify_severity(response_text)

    summary = f"[FUZZ-AI]\nPayload: {payload}\nURL: {url}\nΔ: {size_diff}\nReflected: {reflected}\n\n"
    summary += f"[SEVERITY]: {severity}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}"
    save_ai_report_to_pdf(summary, site=url)
from core.generate_pdf import generate_ai_pdf
from openai import OpenAI

client = OpenAI()

def ai_trigger_if_needed(payload, response_text, url, reflected=False, size_diff=0):
    if not reflected and abs(size_diff) < 50:
        return  # ništa posebno, preskoči

    print("[AI] Analiziram potencijalnu ranjivost...")

    prompt = f"""
URL: {url}
Payload: {payload}
Response: {response_text[:1000]}

Analiziraj da li payload predstavlja ranjivost. Ako da, napiši:
- Eksploataciju
- Predlog za ispravku
- Ozbiljnost (SEVERITY)

Vrati u JSON:
{{
  "exploit": "...",
  "fix": "...",
  "severity": "LOW|MEDIUM|HIGH"
}}
"""

    try:
        result = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        reply = result.choices[0].message.content.strip()
        parsed = json.loads(reply)

        generate_ai_pdf(
            payload=payload,
            url=url,
            output=response_text[:1000],
            exploit=parsed["exploit"],
            fix=parsed["fix"],
            severity=parsed["severity"],
            strategy="Auto Trigger via Fuzz",
            agent="ShadowAgentX"
        )

    except Exception as e:
        print(f"[x] AI PDF generacija neuspešna: {e}")
