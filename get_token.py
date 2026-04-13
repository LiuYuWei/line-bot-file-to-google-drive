from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Replace these with your Client ID and Client Secret
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    
    token_info = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": creds.refresh_token,
        "type": "authorized_user"
    }
    
    print("\n--- Copy the JSON content below ---")
    print(json.dumps(token_info, indent=2))
    print("--- End of JSON content ---")

if __name__ == '__main__':
    main()
