import os
import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ТВОИ ДАННЫЕ ИЗ ТЕЛЕГРАМА
TELEGRAM_TOKEN = "8280920495:AAE-KXGDd7wdT3fsxtqFOGBm0bjjF6B0zZw"
YOUR_CHAT_ID = "5929760309"

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/order")
async def create_order(item: str, price: int, phone: str):
    # Текст сообщения для тебя
    message = f"🚀 **НОВЫЙ ЗАКАЗ!**\n\n👕 Товар: {item}\n💰 Цена: {price} руб.\n📞 Телефон: {phone}"
    
    # Отправка в Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": YOUR_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    requests.post(url, json=payload)
    
    print(f"!!! ЗАКАЗ ОТПРАВЛЕН В ТЕЛЕГУ: {item} !!!")
    return {"status": "success"}
