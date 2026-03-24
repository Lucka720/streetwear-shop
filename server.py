import os, json, requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ВСТАВЬ СВОИ ДАННЫЕ СЮДА
TOKEN = "8280920495:AAE-KXGDd7wdT3fsxtqFOGBm0bjjF6B0zZw"
MY_ID = "5929760309"
DB_FILE = "products.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

products = load_db()

@app.route('/')
def index(): return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin(): return send_from_directory('.', 'admin.html')

@app.route('/get-products')
def get_products(): return jsonify(products)

@app.route('/add-product', methods=['POST'])
def add_product():
    data = request.json
    products.append(data)
    save_db(products)
    return jsonify({"status": "ok"})

@app.route('/order', methods=['POST'])
def order():
    d = request.json
    # Собираем подробное сообщение для бота
    text = (
        f"🛍 **НОВЫЙ ЗАКАЗ**\n"
        f"--------------------------\n"
        f"📦 Товар: {d.get('product')}\n"
        f"👤 ФИО: {d.get('fio')}\n"
        f"📞 Тел/ТГ: {d.get('phone')}\n"
        f"📍 Адрес/Индекс: {d.get('address')}\n"
        f"📧 Email: {d.get('email') or 'не указан'}\n"
        f"--------------------------"
    )
    
    # Отправляем в Telegram
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
        json={"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"}
    )
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
