import os
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    # Проверка, видит ли сервер файлы
    if os.path.exists('index.html'):
        return send_from_directory('.', 'index.html')
    return "СЕРВЕР ЗАПУЩЕН, НО index.html НЕ НАЙДЕН В КОРНЕ"

@app.route('/admin')
def admin():
    if os.path.exists('admin.html'):
        return send_from_directory('.', 'admin.html')
    return "ФАЙЛ admin.html ОТСУТСТВУЕТ НА GITHUB"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
