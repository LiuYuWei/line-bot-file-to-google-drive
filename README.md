# LINE Bot to Google Drive Uploader

這是一個開源的 LINE Bot 專案，讓使用者可以透過 LINE 傳送檔案（圖片、影片、音訊、文件），Bot 會自動將這些檔案上傳到指定的 Google Drive 資料夾，並回傳一個「所有人皆可查看」的分享連結。

本專案採用 **FastAPI** 開發，並設計為可輕鬆部署至 **Google Cloud Run**。

## 功能特點
- 自動上傳檔案至 Google Drive。
- 自動設定檔案權限為「知道連結的人皆可檢視」。
- 回傳 Google Drive 分享連結。
- 支援多種檔案格式。
- 容器化設計，支援 Cloud Run 部署。

---

## 準備工作

在開始之前，您需要準備：
1. **LINE Developer 帳號**：建立一個 Messaging API Channel。
2. **Google Cloud Project**：
   - 啟用 **Google Drive API**。
   - 建立一個 **服務帳戶 (Service Account)**。
   - 下載服務帳戶的 **JSON 金鑰檔案**。
3. **Google Drive 資料夾**：
   - 建立一個用於存放上傳檔案的資料夾。
   - **重要：** 將該資料夾分享給您的服務帳戶 Email（具備「編輯者」權限）。

---

## 環境變數設定

請參考 `.env.example` 建立 `.env` 檔案，或在 Cloud Run 中設定以下環境變數：

| 變數名稱 | 說明 |
| --- | --- |
| `LINE_CHANNEL_SECRET` | LINE Messaging API 的 Channel Secret |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Messaging API 的 Channel Access Token |
| `GOOGLE_DRIVE_FOLDER_ID` | Google Drive 資料夾的 ID |
| `GOOGLE_APPLICATION_CREDENTIALS` | (本地開發) 服務帳戶 JSON 檔案路徑 |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | (Cloud Run) 服務帳戶 JSON 的完整字串內容 |

---

## 本地開發

1. 安裝套件：
   ```bash
   pip install -r requirements.txt
   ```
2. 啟動服務：
   ```bash
   python -m src.main
   ```
3. 使用 `ngrok` 將本地服務暴露至公網：
   ```bash
   ngrok http 8080
   ```
4. 將 ngrok 提供之網址填入 LINE Developer Console 的 Webhook URL (需加上 `/callback`)。

---

## 部署至 Google Cloud Run

使用以下指令進行部署：

```bash
gcloud run deploy line-bot-gdrive \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars "LINE_CHANNEL_SECRET=your_secret,LINE_CHANNEL_ACCESS_TOKEN=your_token,GOOGLE_DRIVE_FOLDER_ID=your_folder_id,GOOGLE_SERVICE_ACCOUNT_JSON='$(cat service_account_key.json)'"
```

> **提示：** 在 Cloud Run 中，建議將服務帳戶 JSON 的內容直接放入 `GOOGLE_SERVICE_ACCOUNT_JSON` 環境變數中，以避免檔案管理的問題。

---

## 授權條款
MIT License
