import os, json, requests, base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- НАСТРОЙКИ ---
TOKEN_TG = "8280920495:AAE-KXGDd7wdT3fsxtqFOGBm0bjjF6B0zZw"
MY_ID = 5929760309
GH_TOKEN = os.environ.get("GH_TOKEN") 
REPO = "Lucka720/streetwear-shop" 
ADMIN_PASSWORD = "Qwerty58763" # Для удаления товаров

FILE_PATH = "products.json"

def get_gh_file():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GH_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = base64.b64decode(r.json()['content']).decode('utf-8')
        return json.loads(content), r.json()['sha']
    return [], None

def save_to_gh(data, sha=None):
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GH_TOKEN}"}
    content = base64.b64encode(json.dumps(data, ensure_ascii=False, indent=4).encode('utf-8')).decode('utf-8')
    payload = {"message": "Update products", "content": content}
    if sha: payload["sha"] = sha
    requests.put(url, json=payload, headers=headers)

@app.route('/')
def index(): return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin(): return send_from_directory('.', 'admin.html')

@app.route('/get-products')
def get_products():
    products, _ = get_gh_file()
    return jsonify(products)

@app.route('/add-product', methods=['POST'])
def add_product():
    new_item = request.json
    products, sha = get_gh_file()
    products.append(new_item)
    save_to_gh(products, sha)
    return jsonify({"status": "ok"})

# --- ВОТ ЭТОТ КУСОК Я ДОБАВИЛ ---
@app.route('/delete-product', methods=['POST'])
def delete_product():
    d = request.json
    if d.get('password') != ADMIN_PASSWORD:
        return jsonify({"status": "error", "message": "Wrong password"}), 403
    
    products, sha = get_gh_file()
    index = d.get('index')
    
    if 0 <= index < len(products):
        products.pop(index) 
        save_to_gh(products, sha)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400
# --- КОНЕЦ НОВОГО КУСКА ---

@app.route('/order', methods=['POST'])
def order():
    d = request.json
    text = f"🛍 НОВЫЙ ЗАКАЗ!\nТовар: {d.get('product')}\n👤 ФИО: {d.get('fio')}\n📞 Тел: {d.get('phone')}\n📍 Адрес: {d.get('address')}\n📧 Email: {d.get('email')}"
    requests.post(f"https://api.telegram.org/bot{TOKEN_TG}/sendMessage", json={"chat_id": MY_ID, "text": text})
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
