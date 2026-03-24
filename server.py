import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ТВОИ ДАННЫЕ (подставь свой токен и ID)
TOKEN = "8280920495:AAE-KXGDd7wdT3fsxtqFOGBm0bjjF6B0zZw"
MY_ID = "5929760309"

products = []

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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
    text = f"🛍 ЗАКАЗ: {data.get('product')}\n👤 ФИО: {data.get('fio')}\n📞 Тел: {data.get('phone')}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": MY_ID, "text": text})
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
