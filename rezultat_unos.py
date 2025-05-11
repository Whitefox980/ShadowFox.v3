import os
from datetime import datetime

TOOLS = {
    "1": "XSS Scanner",
    "2": "SQL Injection",
    "3": "IDOR Checker",
    "4": "LFI Scanner",
    "5": "SSRF Tester",
    "6": "Command Injection",
    "7": "Open Redirect",
    "8": "Subdomain Enum",
    "9": "Custom Radar"
}

print("Odaberi alat:")
for k, v in TOOLS.items():
    print(f"{k}. {v}")

tool_choice = input("Broj alata: ").strip()
tool_name = TOOLS.get(tool_choice, "UnknownTool")

url = input("Unesi URL mete: ").strip()
host = url.replace("https://", "").replace("http://", "").replace("/", "_")

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"results/{tool_name.lower().replace(' ', '_')}_{host}_{timestamp}.txt"

os.makedirs("results", exist_ok=True)

with open(filename, "w") as f:
    f.write(f"# Alat: {tool_name}\n")
    f.write(f"# Meta: {url}\n")
    f.write(f"# Datum: {timestamp.replace('_', ' ')}\n\n")
    f.write("[Rezultat]\n")
    f.write("(Ovde unesi ručno zalepljen output skeniranja...)\n\n")
    f.write("[Status]\n")
    f.write("success | fail | warning\n")

print(f"\nFajl je kreiran: {filename}")
print("Otvori ga i nalepi rezultat u [Rezultat] sekciji.")
