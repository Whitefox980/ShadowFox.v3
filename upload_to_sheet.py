import os
import gspread
from google.oauth2.service_account import Credentials

# Putanja do JSON fajla
SERVICE_ACCOUNT_FILE = "boxwood-airport-458920-e1-8dac401546e1.json"
SHEET_NAME = "BugHuntLog"  # Ovde stavi tačan naziv tvog Google Sheet dokumenta

# Scopes za Sheets i Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Autentifikacija
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE
).with_scopes(SCOPES)
client = gspread.authorize(creds)

# Otvori sheet
sheet = client.open(SHEET_NAME).sheet1

# Test log linije
logs = [
    ["Datum", "Skripta", "Rezultat"],
    ["2024-05-05", "poc_scripts/xss_scanner.py", "XSS pronađen na liniji 24"],
    ["2024-05-05", "poc_scripts/sql_injection.py", "Nema ranjivosti"]
]

# Unesi redove u sheet
for i, row in enumerate(logs):
    sheet.insert_row(row, index=i+1)

print("Uspešno upisano u Google Sheet.")
