# logics/log_utils.py
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SERVICE_ACCOUNT_FILE = "boxwood-airport-458920-e1-8dac401546e1.json"
SHEET_NAME = "BugHuntLog"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def log_to_sheet(script_name, result):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE
    ).with_scopes(SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.insert_row([now, script_name, result], index=2)
    print(f"[+] Log upisan za {script_name}")
