import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ТВОИ ДАННЫЕ (подставь свои из бота)
TOKEN = "8280920495:AAE-KXGDd7wdT3fsxtqFOGBm0bjjF6B0zZw"
MY_ID = "5929760309"

# Список товаров
products = []

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ВОТ ЭТОТ КУСОК ОЖИВИТ ССЫЛКУ /admin
@app.route('/admin')
def admin_page():
    return send_from_directory('.', 'admin.html')

@app.route('/get-products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/add-product', methods=['POST'])
def add_product():
    data = request.json
    products.append(data)
    return jsonify({"status": "ok"})

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    text = (
        f"🛍 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"📦 **Товар:** {data.get('product')}\n"
        f"👤 **ФИО:** {data.get('fio')}\n"
        f"📞 **Связь:** {data.get('phone')}\n"
        f"📍 **Адрес:** {data.get('address')}\n"
        f"📧 **Email:** {data.get('email', 'Не указан')}"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"})
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
