import os
import sys
from fastapi import FastAPI, Request, HTTPException
from linebot.exceptions import InvalidSignatureError
from .line_handler import handler

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "LINE Bot GDrive Uploader is running!"}

@app.post("/callback")
async def callback(request: Request):
    # Get X-Line-Signature header value
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="X-Line-Signature header is missing.")

    # Get request body as text
    body = await request.body()
    body_str = body.decode("utf-8")

    # Handle webhook body
    try:
        handler.handle(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature. Check your channel secret.")
    except Exception as e:
        print(f"Error handling webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

    return "OK"

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
