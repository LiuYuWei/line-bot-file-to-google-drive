# LINE Bot to Google Drive Uploader

This tool allows you to automatically save files (photos, videos, audio, documents) sent via LINE messages directly to your Google Drive. After uploading, the bot replies with a shareable link, making it easy to share content with others instantly.

This project is optimized for **Personal @gmail.com accounts**, solving the common "Storage Quota Exceeded" issue.

---

## 🛠️ Prerequisites

Before you start, you need to complete the following three parts of configuration:

### Part 1: LINE Bot Setup
1. Log in to the [LINE Developers Console](https://developers.line.biz/).
2. Create a **Messaging API Channel**.
3. Under the "Messaging API" tab, obtain the following two pieces of information:
   - **Channel secret**
   - **Channel access token** (click "Issue" to generate)

### Part 2: Google Cloud Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. **Create a Project**: Click the menu at the top to create a new project.
3. **Enable APIs**: Search for and enable **"Google Drive API"**.
4. **OAuth Consent Screen**:
   - Search for "OAuth consent screen", choose "External".
   - Fill in the app name and your email.
   - In the "Test users" section, click **ADD USERS** and add your own @gmail.com address.
5. **Create Credentials**:
   - Go to the "Credentials" page.
   - Click "Create Credentials" > **"OAuth client ID"**.
   - Choose **"Desktop App"** as the application type.
   - After creation, note your **Client ID** and **Client Secret**.

### Part 3: Obtain Authorization Token (Crucial Step)
To allow the bot to upload files "on your behalf," you need to generate a specific key:
1. Download this project and find `get_token.py` in the local folder.
2. Open it with a text editor and paste your `CLIENT_ID` and `CLIENT_SECRET` into the designated fields.
3. Run in your terminal: `make get-token`.
4. A browser window will pop up. Choose your Google account and allow access.
5. After successful authorization, the terminal will output a **JSON string**. **Copy this entire string.**

---

## 🚀 Deployment (Using Google Cloud Run)

This project is designed for quick deployment to Google Cloud Run, a cloud environment that keeps your bot online 24/7.

1. **Prepare Environment File**:
   Create a file named `env.yaml` with the following content:
   ```yaml
   LINE_CHANNEL_SECRET: "Your Secret"
   LINE_CHANNEL_ACCESS_TOKEN: "Your Token"
   GOOGLE_DRIVE_FOLDER_ID: "Google Drive Folder ID"
   GOOGLE_SERVICE_ACCOUNT_JSON: 'Paste the JSON string obtained from Part 3 here'
   ```
   *(Note: The Folder ID is the string after `folders/` in your Drive folder URL)*

2. **Execute Deployment Command**:
   In your terminal (ensure Google Cloud SDK is installed), run:
   ```bash
   gcloud run deploy line-bot-gdrive \
     --source . \
     --platform managed \
     --region asia-east1 \
     --allow-unauthenticated \
     --env-vars-file env.yaml
   ```

3. **Set Webhook**:
   Once deployed, you will receive a **Service URL**. Go back to the LINE Developers Console:
   - Set the Webhook URL to: `YOUR_URL/callback`
   - Enable the **Use Webhook** switch.

---

## 📂 File Structure
- `src/main.py`: Entry point for receiving LINE messages.
- `src/gdrive_service.py`: Logic for uploading files to Google Drive.
- `get_token.py`: Helper tool for safely obtaining personal authorization.
- `Makefile`: Shortcut commands for advanced users.

---

## ⚖️ License
This project is licensed under the Apache License 2.0. Feel free to use, modify, and share.
