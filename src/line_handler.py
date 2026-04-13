import os
import uuid
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, 
    ImageMessage, 
    VideoMessage, 
    AudioMessage, 
    FileMessage,
    TextMessage, 
    TextSendMessage
)
from .config import settings
from .gdrive_service import gdrive_service

# Initialize LINE Bot SDK
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage, FileMessage))
def handle_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    
    # Get file details
    if isinstance(event.message, FileMessage):
        filename = event.message.file_name
        mime_type = 'application/octet-stream'
    elif isinstance(event.message, ImageMessage):
        filename = f"{uuid.uuid4()}.jpg"
        mime_type = 'image/jpeg'
    elif isinstance(event.message, VideoMessage):
        filename = f"{uuid.uuid4()}.mp4"
        mime_type = 'video/mp4'
    elif isinstance(event.message, AudioMessage):
        filename = f"{uuid.uuid4()}.m4a"
        mime_type = 'audio/x-m4a'
    else:
        return # Should not happen with the decorator filter

    # Inform user that we're uploading
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="檔案上傳中，請稍候...")
    )

    try:
        # Collect chunks into binary data
        file_bytes = b''
        for chunk in message_content.iter_content():
            file_bytes += chunk
        
        # Upload to Google Drive
        drive_link = gdrive_service.upload_file(file_bytes, filename, mime_type)
        
        # Send back the link
        line_bot_api.push_message(
            event.source.user_id,
            [
                TextSendMessage(text="檔案已成功上傳至 Google Drive！\n您可以分享以下連結給其他人使用："),
                TextSendMessage(text=f"{drive_link}")
            ]
        )
    except Exception as e:
        print(f"Error during upload: {e}")
        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text=f"上傳失敗，請稍後再試。錯誤資訊：{str(e)}")
        )
