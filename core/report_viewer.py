import os
import re

def list_reports():
    reports = [f for f in os.listdir("reports") if f.endswith(".pdf")]
    if not reports:
        print("[x] Nema generisanih PDF izveštaja.")
        return []

    print("\n[+] Dostupni AI izveštaji:")
    for i, f in enumerate(reports, 1):
        print(f"{i:02d}. {f}")
    return reports

def open_report(filename):
    try:
        import platform
        system = platform.system()
        if system == "Linux":
            os.system(f"xdg-open reports/{filename}")
        elif system == "Darwin":
            os.system(f"open reports/{filename}")
        elif system == "Windows":
            os.startfile(f"reports/{filename}")
    except:
        print("[x] Ne mogu da otvorim PDF automatski.")

def search_in_reports(term):
    print(f"\n[?] Tražim '{term}' u izveštajima...")
    for fname in os.listdir("reports"):
        if not fname.endswith(".pdf"):
            continue
        path = os.path.join("reports", fname)
        try:
            with open(path, "rb") as f:
                content = f.read().decode("utf-8", errors="ignore")
                if term.lower() in content.lower():
                    print(f"[✓] Pronađeno u: {fname}")
        except:
            continue
