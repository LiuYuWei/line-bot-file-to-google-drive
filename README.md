# LINE Bot 雲端硬碟自動上傳工具 (LINE Bot to Google Drive Uploader)

這是一個讓您可以透過 LINE 訊息，直接將檔案（照片、影片、音訊、文件）轉存到 Google Drive 雲端硬碟的自動化工具。上傳後，Bot 會自動回傳一個「具備檢視權限」的分享連結，方便您快速分享給他人。

本專案特別針對 **個人 @gmail.com 帳號** 優化，解決了常見的「儲存空間配額不足」問題。

---

## 🛠️ 準備工作

在開始之前，您需要完成以下三個部分的設定：

### 第一部分：LINE 機器人設定
1. 前往 [LINE Developers Console](https://developers.line.biz/) 並登入。
2. 建立一個 **Messaging API Channel**。
3. 在 「Messaging API」 分頁中，取得以下兩項資訊：
   - **Channel secret**
   - **Channel access token** (點擊 Issue 產生)

### 第二部分：Google 雲端設定
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)。
2. **建立專案**：點擊上方選單建立一個新專案。
3. **啟用服務**：搜尋並啟用 **「Google Drive API」**。
4. **OAuth 同意畫面**：
   - 搜尋「OAuth consent screen」，選擇「外部 (External)」。
   - 填寫應用程式名稱與您的 Email。
   - 在「測試使用者 (Test users)」區塊，點擊 **ADD USERS** 並加入您自己的 @gmail.com。
5. **建立憑證**：
   - 前往「憑證 (Credentials)」頁面。
   - 點擊「建立憑證」 > **「OAuth 用戶端 ID」**。
   - 應用程式類型選擇 **「桌面應用程式 (Desktop App)」**。
   - 建立後，請記下您的 **用戶端 ID (Client ID)** 與 **用戶端密鑰 (Client Secret)**。

### 第三部分：取得授權金鑰 (最重要的一步)
為了讓 Bot 能「代表您」上傳檔案，我們需要產生一組專屬金鑰：
1. 下載本專案並在本地資料夾找到 `get_token.py`。
2. 用文字編輯器開啟它，將您的 `CLIENT_ID` 與 `CLIENT_SECRET` 貼入對應位置。
3. 在終端機執行：`make get-token`。
4. 瀏覽器會跳出授權視窗，請選擇您的 Google 帳號並允許存取。
5. 授權成功後，終端機會輸出一串 **JSON 內容**。**請完整複製這段內容。**

---

## 🚀 部署教學 (使用 Google Cloud Run)

本專案設計為可快速部署至 Google Cloud Run，這是一個雲端執行環境，讓您的機器人 24 小時在線。

1. **準備環境變數檔案**：
   建立一個名為 `env.yaml` 的檔案，內容如下：
   ```yaml
   LINE_CHANNEL_SECRET: "您的 Secret"
   LINE_CHANNEL_ACCESS_TOKEN: "您的 Token"
   GOOGLE_DRIVE_FOLDER_ID: "Google Drive 資料夾的 ID"
   GOOGLE_SERVICE_ACCOUNT_JSON: '將剛才步驟三取得的 JSON 內容整串貼在這裡'
   ```
   *(註：資料夾 ID 位於該雲端硬碟網址中 `folders/` 後面的字串)*

2. **執行部署指令**：
   在終端機輸入（確保已安裝 Google Cloud SDK）：
   ```bash
   gcloud run deploy line-bot-gdrive \
     --source . \
     --platform managed \
     --region asia-east1 \
     --allow-unauthenticated \
     --env-vars-file env.yaml
   ```

3. **設定 Webhook**：
   部署成功後，您會得到一個 **Service URL**。請回到 LINE Developers Console：
   - 將 Webhook URL 設定為：`您的網址/callback`
   - 開啟 **Use Webhook** 開關。

---

## 📂 檔案結構說明
- `src/main.py`: 接收 LINE 訊息的入口。
- `src/gdrive_service.py`: 處理檔案上傳至 Google Drive 的邏輯。
- `get_token.py`: 輔助工具，協助您安全地取得個人授權。
- `Makefile`: 捷徑指令集，方便進階使用者操作。

---

## ⚖️ 授權條款
本專案採用 Apache License 2.0 授權條款，歡迎自由使用、修改與分享。
