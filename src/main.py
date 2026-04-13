import os
import sys
from fastapi import FastAPI, Request, HTTPException
from linebot.exceptions import InvalidSignatureError
from .line_handler import handler

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "LINE Bot GDrive Uploader is running!"}

@app.get("/callback")
async def callback_get():
    return {"status": "OK", "message": "Callback endpoint is ready for POST requests from LINE."}

@app.post("/callback")
async def callback(request: Request):
    # Get X-Line-Signature header value
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        # Some verification tools might not send signature, return 200 to pass simple checks
        print("X-Line-Signature header is missing. This might be a verification test.")
        return "OK"

    # Get request body as text
    body = await request.body()
    body_str = body.decode("utf-8")

    # Handle webhook body
    try:
        handler.handle(body_str, signature)
    except InvalidSignatureError:
        print("Invalid signature. Check your channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature.")
    except Exception as e:
        print(f"Error handling webhook: {e}")
        # Return 200 even on some errors to prevent LINE from retrying too many times during testing
        return "OK"

    return "OK"

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
