import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ТВОИ ДАННЫЕ (Убедись, что они верные!)
TOKEN = "8280920495:AAE-KXGDd7wdT3fsxtqFOGBm0bjjF6B0zZw"
MY_ID = "5929760309"

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    
    # Собираем красивое сообщение для Тебя
    text = (
        f"🛍 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"📦 **Товар:** {data.get('product')}\n"
        f"👤 **ФИО:** {data.get('fio')}\n"
        f"📞 **Связь:** {data.get('phone')}\n"
        f"📍 **Адрес:** {data.get('address')}\n"
        f"📧 **Email:** {data.get('email') if data.get('email') else 'Не указан'}"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, json=payload)
        if response.ok:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "details": response.text}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
