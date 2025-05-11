import json
from datetime import datetime

def ask_ai(question: str) -> dict:
    # Ovo je mock – zameniti pravim AI pozivom ako želiš
    return {
        "question": question,
        "answer": f"Simuliran odgovor na: {question}",
        "timestamp": datetime.utcnow().isoformat()
    }

def save_to_log(entry: dict, log_path="data/logs/bughunt_log.jsonl"):
    with open(log_path, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    while True:
        q = input(">>> Pitaj AI (ili 'exit'): ").strip()
        if q.lower() == "exit":
            break
        response = ask_ai(q)
        print(f"AI: {response['answer']}")
        save_to_log(response)

if __name__ == "__main__":
    main()
# 3. Generisanje izveštaja na osnovu rezultata
log("\n[+] Generišem završni izveštaj...")
try:
    subprocess.run(["python", "logics/generate_report.py"], check=True)
    log("[+] Izveštaj uspešno generisan.")
except subprocess.CalledProcessError:
    log("[-] Greška prilikom generisanja izveštaja.")
# Upload na Google Drive
log("\n[+] Upload rezultata na Google Drive...")
try:
    from drive_upload import upload_results_to_drive
    upload_results_to_drive()
    log("[+] Upload uspešan.")
except Exception as e:
    log(f"[-] Greska prilikom upload-a: {e}")
