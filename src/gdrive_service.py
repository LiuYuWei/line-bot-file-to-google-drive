import io
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from .config import settings

class GoogleDriveService:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive.file']
        self.creds = self._authenticate()
        self.service = build('drive', 'v3', credentials=self.creds)

    def _authenticate(self):
        """
        Authenticate with Google Drive using OAuth 2.0 (Refresh Token).
        """
        if settings.GOOGLE_SERVICE_ACCOUNT_JSON:
            try:
                info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
                # Check if it's an OAuth2 token JSON (authorized_user)
                if info.get('type') == 'authorized_user':
                    return service_account.Credentials.from_service_account_info(
                        info, scopes=self.scopes
                    )
                # Handle standard service account
                return service_account.Credentials.from_service_account_info(
                    info, scopes=self.scopes
                )
            except Exception as e:
                # If from_service_account_info fails, try User Credentials (OAuth2)
                try:
                    from google.oauth2.credentials import Credentials
                    info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
                    return Credentials(
                        None,
                        refresh_token=info.get('refresh_token'),
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=info.get('client_id'),
                        client_secret=info.get('client_secret'),
                        scopes=self.scopes
                    )
                except Exception as e2:
                    print(f"Error during OAuth2 authentication: {e2}")
        
        raise Exception("Google credentials not found or invalid.")

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
            fields='id, webViewLink',
            supportsAllDrives=True
        ).execute()
        
        file_id = file.get('id')
        
        # 2. Update permissions to 'anyone with the link can view'
        self.service.permissions().create(
            fileId=file_id,
            body={
                'type': 'anyone',
                'role': 'reader'
            },
            supportsAllDrives=True
        ).execute()
        
        # 3. Retrieve the updated webViewLink
        file = self.service.files().get(
            fileId=file_id,
            fields='webViewLink',
            supportsAllDrives=True
        ).execute()
        
        return file.get('webViewLink')

gdrive_service = GoogleDriveService()
