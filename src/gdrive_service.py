import io
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from .config import settings

class GoogleDriveService:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.creds = self._authenticate()
        self.service = build('drive', 'v3', credentials=self.creds)

    def _authenticate(self):
        """
        Authenticate with Google Service Account using JSON content string or file path.
        """
        if settings.GOOGLE_SERVICE_ACCOUNT_JSON:
            try:
                info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
                return service_account.Credentials.from_service_account_info(
                    info, scopes=self.scopes
                )
            except Exception as e:
                print(f"Error parsing GOOGLE_SERVICE_ACCOUNT_JSON: {e}")
        
        # Fallback to file path (GOOGLE_APPLICATION_CREDENTIALS)
        if settings.GOOGLE_APPLICATION_CREDENTIALS:
            return service_account.Credentials.from_service_account_file(
                settings.GOOGLE_APPLICATION_CREDENTIALS, scopes=self.scopes
            )
            
        raise Exception("Google credentials not found in environment.")

    def upload_file(self, file_content: bytes, filename: str, mime_type: str):
        """
        Upload file content to Google Drive and return the shareable link.
        """
        file_metadata = {
            'name': filename,
            'parents': [settings.GOOGLE_DRIVE_FOLDER_ID]
        }
        
        fh = io.BytesIO(file_content)
        media = MediaIoBaseUpload(fh, mimetype=mime_type, resumable=True)
        
        # 1. Upload the file
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        file_id = file.get('id')
        
        # 2. Update permissions to 'anyone with the link can view'
        self.service.permissions().create(
            fileId=file_id,
            body={
                'type': 'anyone',
                'role': 'reader'
            }
        ).execute()
        
        # 3. Retrieve the updated webViewLink
        file = self.service.files().get(
            fileId=file_id,
            fields='webViewLink'
        ).execute()
        
        return file.get('webViewLink')

gdrive_service = GoogleDriveService()
