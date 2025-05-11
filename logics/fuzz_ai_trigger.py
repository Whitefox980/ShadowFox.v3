import os

USE_AI = os.getenv("DISABLE_AI", "0") != "1"

if USE_AI:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
else:
    client = None

from logics.ai_tools import suggest_exploit, suggest_fix, classify_severity
from core.generate_pdf import generate_ai_pdf

def ai_trigger_if_needed(payload, response_text, url, reflected=False, size_diff=0):
    if not USE_AI or client is None:
        return "AI DISABLED"

    if not reflected and abs(size_diff) < 30:
        return

    print("\n[AI] Uslov zadovoljen, pokrećem analizu...")

    exploit = suggest_exploit(response_text)
    fix = suggest_fix(response_text)
    severity = classify_severity(response_text)

    summary = (
        f"[FUZZ-AI]\nPayload: {payload}\nURL: {url}\nΔ: {size_diff}\nReflected: {reflected}"
        f"\n\n[SEVERITY]: {severity}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}"
    )

    generate_ai_pdf(summary, site=url)

