import os
import requests
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

TELEGRAM_TOKEN = "8280920495:AAE-KXGDd7wdT3fsxtqFOGBm0bjjF6B0zZw"
YOUR_CHAT_ID = "5929760309"

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/order")
async def create_order(item: str = Form(...), phone: str = Form(...)):
    message = f"🚀 **НОВЫЙ ЗАКАЗ!**\n\n👕 Товар: {item}\n📞 Телефон: {phone}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": YOUR_CHAT_ID, "text": message, "parse_mode": "Markdown"})
    
    return {"status": "success"}
