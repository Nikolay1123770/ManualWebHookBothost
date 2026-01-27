import os
import json
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
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# Выводим информацию при запуске
logger.info("=" * 60)
logger.info("TELEGRAM BOT STARTING")
logger.info("=" * 60)
logger.info(f"Token present: {'YES' if TOKEN else 'NO'}")
logger.info(f"Webhook URL: {WEBHOOK_URL}")

@app.route('/')
def home():
    """Главная страница"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot Control</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            .button {
                display: inline-block;
                padding: 10px 20px;
                margin: 10px 5px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                border: none;
                cursor: pointer;
            }
            .button:hover { background: #0056b3; }
            .status {
                padding: 15px;
                margin: 15px 0;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 4px solid #007bff;
            }
            pre {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
        <h1>🤖 Telegram Bot Control Panel</h1>
        
        <div class="status">
            <p><strong>Webhook URL:</strong> <code>""" + WEBHOOK_URL + """</code></p>
            <p><strong>Token:</strong> <code>""" + (TOKEN[:10] + "..." if TOKEN else "NOT SET") + """</code></p>
        </div>
        
        <h3>Actions:</h3>
        <button class="button" onclick="action('test_bot')">Test Bot Token</button>
        <button class="button" onclick="action('setup_webhook')">Setup Webhook</button>
        <button class="button" onclick="action('check_webhook')">Check Webhook</button>
        <button class="button" onclick="action('delete_webhook')">Delete Webhook</button>
        
        <div class="status">
            <h3>Instructions:</h3>
            <ol>
                <li>Click "Test Bot Token" - should show <code>"ok": true</code></li>
                <li>Click "Setup Webhook" - should show success</li>
                <li>Click "Check Webhook" - should show URL: <code>""" + WEBHOOK_URL + """</code></li>
                <li>Open Telegram and send <code>/start</code> to your bot</li>
            </ol>
        </div>
        
        <div id="result" class="status">
            <h3>Result:</h3>
            <p>Click a button above to see results here</p>
        </div>
        
        <script>
        function action(endpoint) {
            document.getElementById('result').innerHTML = '<p>Loading...</p>';
            fetch('/' + endpoint)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerHTML = 
                        '<h3>Result:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                })
                .catch(error => {
                    document.getElementById('result').innerHTML = 
                        '<h3>Error:</h3><p>' + error + '</p>';
                });
        }
        </script>
    </body>
    </html>
    """

@app.route('/test_bot')
def test_bot():
    """Проверка токена бота"""
    if not TOKEN:
        return jsonify({"ok": False, "error": "Token not set"})
    
    try:
        response = requests.get(f"{TELEGRAM_API}/getMe", timeout=10)
        return response.json()
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/setup_webhook')
def setup_webhook():
    """Установка вебхука"""
    if not TOKEN:
        return jsonify({"ok": False, "error": "Token not set"})
    
    try:
        response = requests.get(f"{TELEGRAM_API}/setWebhook?url={WEBHOOK_URL}", timeout=10)
        data = response.json()
        logger.info(f"Webhook setup result: {data}")
        return data
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/check_webhook')
def check_webhook():
    """Проверка статуса вебхука"""
    if not TOKEN:
        return jsonify({"ok": False, "error": "Token not set"})
    
    try:
        response = requests.get(f"{TELEGRAM_API}/getWebhookInfo", timeout=10)
        return response.json()
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/delete_webhook')
def delete_webhook():
    """Удаление вебхука"""
    if not TOKEN:
        return jsonify({"ok": False, "error": "Token not set"})
    
    try:
        response = requests.get(f"{TELEGRAM_API}/deleteWebhook", timeout=10)
        return response.json()
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """
    Обработчик вебхука от Telegram
    ПОЛНОСТЬЮ СИНХРОННАЯ ФУНКЦИЯ
    """
    try:
        # Получаем данные
        data = request.get_json()
        
        # Логируем входящие данные
        logger.info(f"📨 Received webhook: {json.dumps(data, ensure_ascii=False)[:200]}...")
        
        # Если нет токена, просто возвращаем ok
        if not TOKEN:
            logger.error("Token not configured")
            return jsonify({"ok": True})
        
        # Обрабатываем сообщение
        if 'message' in data:
            message = data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '').strip()
            
            logger.info(f"💬 Message from {chat_id}: {text}")
            
            # Формируем ответ
            response_text = ""
            if text == '/start':
                response_text = (
                    "🎉 Привет! Я бот на bothost!\n\n"
                    "✅ Вебхук успешно подключен\n"
                    "🌐 Домен: manualwebhookbothost.bothost.ru\n\n"
                    "Команды:\n"
                    "/help - помощь\n"
                    "/status - статус\n"
                    "/test - тест"
                )
            elif text == '/help':
                response_text = "Помощь: это тестовый бот на платформе bothost"
            elif text == '/status':
                response_text = f"Статус: ✅ Работает\nWebhook: {WEBHOOK_URL}"
            elif text == '/test':
                response_text = "✅ Тест пройден! Бот работает!"
            elif text:
                response_text = f"📝 Вы написали: {text}"
            
            # Отправляем ответ если есть что отправлять
            if response_text:
                # Отправляем сообщение через Telegram API
                send_to_telegram(chat_id, response_text)
        
        # Всегда возвращаем успех
        return jsonify({"ok": True})
        
    except Exception as e:
        logger.error(f"❌ Error in webhook handler: {e}")
        # Все равно возвращаем ok, чтобы Telegram не считал доставку неудачной
        return jsonify({"ok": True})

def send_to_telegram(chat_id, text):
    """Отправка сообщения в Telegram"""
    try:
        response = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            logger.info(f"✅ Sent message to {chat_id}")
        else:
            logger.error(f"❌ Failed to send message: {response.text}")
            
    except Exception as e:
        logger.error(f"❌ Error sending to Telegram: {e}")

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "telegram-bot",
        "webhook_url": WEBHOOK_URL,
        "token_set": bool(TOKEN)
    })

if __name__ == '__main__':
    # Автоматически устанавливаем вебхук при запуске
    if TOKEN:
        try:
            logger.info("🔧 Setting up webhook automatically...")
            response = requests.get(f"{TELEGRAM_API}/setWebhook?url={WEBHOOK_URL}", timeout=10)
            logger.info(f"🔧 Webhook setup result: {response.json()}")
            
            # Проверяем бота
            bot_info = requests.get(f"{TELEGRAM_API}/getMe", timeout=10).json()
            if bot_info.get('ok'):
                logger.info(f"🤖 Bot @{bot_info['result']['username']} is ready!")
            else:
                logger.error(f"❌ Bot error: {bot_info.get('description')}")
                
        except Exception as e:
            logger.error(f"⚠️ Startup error: {e}")
    else:
        logger.error("❌ TELEGRAM_TOKEN is not set! Bot will not work.")
    
    # Запускаем сервер
    port = int(os.environ.get('PORT', 3000))
    logger.info(f"🚀 Starting server on port {port}")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False)
