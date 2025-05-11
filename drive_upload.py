# drive_upload.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Podesi ove vrednosti
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Ovo ti je JSON fajl sa Google API Console
FOLDER_ID = 'TVOJA_FOLDER_ID'  # ID fascikle na GDrive

def upload_results_to_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=creds)

    results_dir = 'results'
    for fname in os.listdir(results_dir):
        fpath = os.path.join(results_dir, fname)
        if os.path.isfile(fpath):
            file_metadata = {
                'name': fname,
                'parents': [FOLDER_ID]
            }
            media = MediaFileUpload(fpath, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"[+] Uploadovan: {fname}")
