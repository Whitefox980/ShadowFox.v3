# utils/log_utils.py

import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from utils.log_utils import log_to_txt, classify_severity
# Google Sheet podešavanja
SHEET_NAME = "BugHuntLog"
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
KEY_FILE = "boxwood-airport-458920-e1-8dac401546e1.json"

def log_to_sheet(script_path, result):
    creds = Credentials.from_service_account_file(KEY_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now, script_path, result[:500]]  # Ograniči prikaz rezultata na 500 karaktera
    sheet.append_row(row)
def classify_severity(result: str) -> str:
    result = result.lower()
    if "sql" in result or "auth bypass" in result:
        return "Critical"
    elif "idor" in result or "rfi" in result:
        return "High"
    elif "lfi" in result or "xss" in result:
        return "Medium"
    elif "refleksije" in result or "parametar" in result:
        return "Low"
    return "Unknown"
import json

def log_to_json(vuln_dict, json_path="results/json/vulnerabilities_export.json"):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    try:
        # Ako fajl postoji, učitaj postojeće ranjivosti
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(vuln_dict)

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"[+] Ranjivost upisana u JSON: {vuln_dict.get('target')}")

    except Exception as e:
        print(f"[-] Greška pri upisu u JSON: {str(e)}")
def log_to_txt(script_name, content):
    with open("shadowfox_log.txt", "a") as f:
        f.write(f"\n\n=== {script_name} ===\n{content}")
