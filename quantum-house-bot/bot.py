import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# ============================================================
# НАСТРОЙКИ
# ============================================================
TOKEN = "8984050158:AAHXubXN-cpMFGqWgSI3zp4u5Cp_1ZC3RRQ"

ADMIN_CHAT_IDS = [
    "5215555078", 
    "8742170642"
]

# ============================================================
# ЛОГИРОВАНИЕ
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)

def send_to_telegram(name, email, message):
    """Отправляет сообщение ВСЕМ админам"""
    text = f"""
📩 <b>Новое сообщение с сайта!</b>

👤 <b>Имя:</b> {name}
📧 <b>Email:</b> {email}
📝 <b>Сообщение:</b>
{message}
    """.strip()
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "text": text,
        "parse_mode": "HTML"
    }
    
    sent_count = 0
    for chat_id in ADMIN_CHAT_IDS:
        data["chat_id"] = chat_id
        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                sent_count += 1
                app.logger.info(f"✅ Сообщение отправлено админу {chat_id}")
            else:
                app.logger.error(f"❌ Ошибка админу {chat_id}: {response.status_code}")
        except Exception as e:
            app.logger.error(f"❌ Ошибка админу {chat_id}: {e}")
    
    return {"success": sent_count > 0, "sent_to": sent_count}

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
        
        result = send_to_telegram(name, email, message)
        
        return jsonify({
            "success": True,
            "message": f"Сообщение отправлено {result['sent_to']} админам"
        })
        
    except Exception as e:
        app.logger.error(f"Ошибка: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================================
# ЗАПУСК
# ============================================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Бот запущен на порту {port}")
    print(f"📩 Сообщения получат {len(ADMIN_CHAT_IDS)} админов:")
    for chat_id in ADMIN_CHAT_IDS:
        print(f"   - {chat_id}")
    app.run(host='0.0.0.0', port=port, debug=False)
