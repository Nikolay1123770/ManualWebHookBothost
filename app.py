import os
import logging
from flask import Flask, request, jsonify
import requests

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация Flask
app = Flask(__name__)

# Конфигурация
TOKEN = os.environ.get('TELEGRAM_TOKEN', '8506600032:AAEGyei4Il9al_dcCnLOxcZDsrT6M8NgeIA')
WEBHOOK_DOMAIN = "https://manualwebhookbothost.bothost.ru"
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}/webhook"

logger.info(f"Bot starting with token: {TOKEN[:10]}...")
logger.info(f"Webhook URL: {WEBHOOK_URL}")

@app.route('/')
def home():
    """Главная страница"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot Status</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }
            .btn { 
                padding: 10px 20px; 
                margin: 5px; 
                background: #4CAF50; 
                color: white; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
            }
            .btn:hover { background: #45a049; }
            .result { 
                margin-top: 20px; 
                padding: 15px; 
                background: #f5f5f5; 
                border-radius: 5px; 
                font-family: monospace; 
            }
        </style>
    </head>
    <body>
        <h1>🤖 Telegram Bot Control Panel</h1>
        
        <div>
            <button class="btn" onclick="testBot()">Test Bot Token</button>
            <button class="btn" onclick="setupWebhook()">Setup Webhook</button>
            <button class="btn" onclick="checkWebhook()">Check Webhook</button>
        </div>
        
        <div id="result" class="result">
            Click a button to test
        </div>
        
        <script>
        function testBot() {
            document.getElementById('result').innerHTML = 'Testing bot...';
            fetch('/test_bot')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                })
                .catch(e => {
                    document.getElementById('result').innerHTML = 'Error: ' + e;
                });
        }
        
        function setupWebhook() {
            document.getElementById('result').innerHTML = 'Setting up webhook...';
            fetch('/setup_webhook')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                })
                .catch(e => {
                    document.getElementById('result').innerHTML = 'Error: ' + e;
                });
        }
        
        function checkWebhook() {
            document.getElementById('result').innerHTML = 'Checking webhook...';
            fetch('/check_webhook')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                })
                .catch(e => {
                    document.getElementById('result').innerHTML = 'Error: ' + e;
                });
        }
        </script>
    </body>
    </html>
    """

@app.route('/test_bot')
def test_bot():
    """Тест токена бота"""
    if not TOKEN:
        return jsonify({"status": "error", "message": "Token not set"})
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=10)
        return response.json()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/setup_webhook')
def setup_webhook():
    """Установка вебхука"""
    if not TOKEN:
        return jsonify({"status": "error", "message": "Token not set"})
    
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}",
            timeout=10
        )
        return response.json()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/check_webhook')
def check_webhook():
    """Проверка вебхука"""
    if not TOKEN:
        return jsonify({"status": "error", "message": "Token not set"})
    
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo",
            timeout=10
        )
        return response.json()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик вебхука от Telegram - ПОЛНОСТЬЮ СИНХРОННЫЙ"""
    try:
        # Получаем данные
        data = request.get_json()
        logger.info(f"Received webhook: {data}")
        
        # Проверяем токен
        if not TOKEN:
            logger.error("Token not configured")
            return jsonify({"ok": False}), 200
        
        # Обрабатываем сообщение
        if 'message' in data:
            message = data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '').strip()
            
            logger.info(f"Processing message from {chat_id}: {text}")
            
            # Формируем ответ
            response_text = ""
            if text == '/start':
                response_text = "✅ Бот работает на bothost с вебхуком!"
            elif text == '/help':
                response_text = "Помощь: /start /help /status"
            elif text == '/status':
                response_text = f"Статус: OK\nДомен: {WEBHOOK_DOMAIN}"
            elif text:
                response_text = f"Вы написали: {text}"
            
            # Отправляем ответ если есть что отправлять
            if response_text:
                send_message(chat_id, response_text)
        
        return jsonify({"ok": True})
        
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

def send_message(chat_id, text):
    """Отправка сообщения в Telegram"""
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=5
        )
        logger.info(f"Sent message to {chat_id}, response: {response.status_code}")
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy", "webhook_url": WEBHOOK_URL})

if __name__ == '__main__':
    # Проверяем конфигурацию при запуске
    print("=" * 60)
    print("TELEGRAM BOT STARTING")
    print("=" * 60)
    
    if TOKEN:
        print(f"Token: {TOKEN[:10]}...")
        
        # Проверяем бота
        try:
            print("Checking bot...")
            bot_info = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=10).json()
            if bot_info.get('ok'):
                print(f"✅ Bot @{bot_info['result']['username']} is valid")
                
                # Устанавливаем вебхук
                print(f"Setting webhook to: {WEBHOOK_URL}")
                webhook_result = requests.get(
                    f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}",
                    timeout=10
                ).json()
                print(f"Webhook result: {webhook_result}")
            else:
                print(f"❌ Bot error: {bot_info.get('description')}")
        except Exception as e:
            print(f"⚠️ Startup error: {e}")
    else:
        print("❌ ERROR: TELEGRAM_TOKEN environment variable is not set!")
        print("Please set TELEGRAM_TOKEN in bothost settings")
    
    # Запускаем сервер
    port = int(os.environ.get('PORT', 3000))
    print(f"\nStarting server on port {port}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False)
