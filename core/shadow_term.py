import os
import re
from collections import Counter
import PyPDF2

def extract_terms():
    terms = []
    common_keywords = [
        "xss", "sql", "sqli", "token", "admin", "bypass", "ssrf", "rce", "root",
        "redirect", "csrf", "open", "upload", "file", "passwd", "localhost",
        "reflected", "severity", "leak", "auth", "cookie"
    ]

    for fname in os.listdir("reports"):
        if not fname.endswith(".pdf"):
            continue
        try:
            with open(os.path.join("reports", fname), "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

                # Pronađi sve relevantne reči
                for word in common_keywords:
                    if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                        terms.append(word.lower())
        except:
            continue

    if not terms:
        print("[x] Nema pronađenih ključnih reči.")
        return

    stats = Counter(terms).most_common()
    print("\n[+] Najčešće ključne reči u AI izveštajima:\n")
    for w, c in stats:
        print(f"{w.upper():10} : {c}x")
