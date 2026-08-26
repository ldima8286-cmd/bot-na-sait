import requests
from flask import Flask, request, jsonify

# ============================================================
# НАСТРОЙКИ (вставь свои данные)
# ============================================================
TOKEN = "8984050158:AAHXubXN-cpMFGqWgSI3zp4u5Cp_1ZC3RRQ"  # ← Токен от BotFather
CHAT_ID = "5215555078"  # ← Твой Telegram ID (от @userinfobot)

# ============================================================
# СОЗДАЁМ ВЕБ-СЕРВЕР
# ============================================================
app = Flask(__name__)

def send_to_telegram(name, email, message):
    """Отправляет сообщение в Telegram"""
    text = f"""
📩 <b>Новое сообщение с сайта!</b>

👤 <b>Имя:</b> {name}
📧 <b>Email:</b> {email}
📝 <b>Сообщение:</b>
{message}
    """.strip()
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ============================================================
# ЭНДПОИНТ ДЛЯ ПРИЁМА СООБЩЕНИЙ С САЙТА
# ============================================================
@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        data = request.get_json()
        
        name = data.get('name', 'Не указано')
        email = data.get('email', 'Не указан')
        message = data.get('message', 'Нет текста')
        
        # Отправляем в Telegram
        result = send_to_telegram(name, email, message)
        
        return jsonify({
            "success": True,
            "message": "Сообщение отправлено в Telegram",
            "telegram_response": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================================
# ЗАПУСК СЕРВЕРА
# ============================================================
if __name__ == '__main__':
    print("🚀 Бот запущен на http://127.0.0.1:5000")
    print(f"📩 Сообщения будут приходить в чат {CHAT_ID}")
    app.run(host='0.0.0.0', port=5000, debug=False)