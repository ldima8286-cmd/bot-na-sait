import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # ← ДОБАВИТЬ
import os

# ============================================================
# НАСТРОЙКИ
# ============================================================
TOKEN = "8984050158:AAHXubXN-cpMFGqWgSI3zp4u5Cp_1ZC3RRQ"
ADMIN_CHAT_ID = "5215555078"

# ============================================================
# СОЗДАЁМ ВЕБ-СЕРВЕР
# ============================================================
app = Flask(__name__)
CORS(app)  # ← РАЗРЕШАЕМ ВСЕ ЗАПРОСЫ С ЛЮБЫХ ДОМЕНОВ

def send_to_telegram(name, email, message):
    """Отправляет сообщение админу в Telegram"""
    text = f"""
📩 <b>Новое сообщение с сайта!</b>

👤 <b>Имя:</b> {name}
📧 <b>Email:</b> {email}
📝 <b>Сообщение:</b>
{message}
    """.strip()
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET'])
def index():
    return "🤖 Бот Quantum House работает!", 200

@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        data = request.get_json()
        
        name = data.get('name', 'Не указано')
        email = data.get('email', 'Не указан')
        message = data.get('message', 'Нет текста')
        
        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "Заполните все поля"
            }), 400
        
        send_to_telegram(name, email, message)
        
        return jsonify({
            "success": True,
            "message": "Сообщение отправлено админу"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Бот запущен на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
