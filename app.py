import os
import logging
from flask import Flask, request
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
TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
# ВАЖНО: Используем .ru а не .app!
WEBHOOK_DOMAIN = "https://manualwebhookbothost.bothost.ru"
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}/webhook"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Telegram Bot Diagnostics</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            .btn {{ padding: 10px 20px; margin: 5px; background: #007bff; color: white; border: none; cursor: pointer; }}
            .btn:hover {{ background: #0056b3; }}
            .success {{ color: green; }}
            .error {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>Диагностика Telegram Bot</h1>
        <p><strong>Домен:</strong> {WEBHOOK_DOMAIN}</p>
        <p><strong>Webhook URL:</strong> {WEBHOOK_URL}</p>
        
        <button class="btn" onclick="testDomain()">1. Проверить домен</button>
        <button class="btn" onclick="setupWebhook()">2. Установить вебхук (.ru)</button>
        <button class="btn" onclick="setupWebhookApp()">3. Установить вебхук (.app)</button>
        <button class="btn" onclick="checkWebhook()">4. Проверить вебхук</button>
        
        <div id="result" style="margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 5px;"></div>
        
        <script>
        async function apiCall(url) {{
            const response = await fetch(url);
            return await response.json();
        }}
        
        function showResult(text) {{
            document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(text, null, 2) + '</pre>';
        }}
        
        async function testDomain() {{
            showResult('Проверяю домен...');
            try {{
                const response = await fetch('{WEBHOOK_DOMAIN}/health');
                const data = await response.json();
                showResult({{domain: '{WEBHOOK_DOMAIN}', status: 'available', response: data}});
            }} catch (error) {{
                showResult({{domain: '{WEBHOOK_DOMAIN}', status: 'not available', error: error.message}});
            }}
        }}
        
        async function setupWebhook() {{
            showResult('Устанавливаю вебхук на .ru домен...');
            try {{
                const response = await fetch('/setup_webhook_ru');
                const data = await response.json();
                showResult(data);
            }} catch (error) {{
                showResult({{error: error.message}});
            }}
        }}
        
        async function setupWebhookApp() {{
            showResult('Устанавливаю вебхук на .app домен...');
            try {{
                const response = await fetch('/setup_webhook_app');
                const data = await response.json();
                showResult(data);
            }} catch (error) {{
                showResult({{error: error.message}});
            }}
        }}
        
        async function checkWebhook() {{
            showResult('Проверяю вебхук...');
            try {{
                const response = await fetch('/check_webhook');
                const data = await response.json();
                showResult(data);
            }} catch (error) {{
                showResult({{error: error.message}});
            }}
        }}
        </script>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "service": "telegram-bot", "domain": WEBHOOK_DOMAIN}

@app.route('/setup_webhook_ru')
def setup_webhook_ru():
    """Установка вебхука на .ru домен"""
    try:
        response = requests.get(f"{BASE_URL}/setWebhook?url={WEBHOOK_URL}")
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/setup_webhook_app')
def setup_webhook_app():
    """Установка вебхука на .app домен (если доступен)"""
    try:
        app_webhook = "https://manualwebhookbothost.bothost.app/webhook"
        response = requests.get(f"{BASE_URL}/setWebhook?url={app_webhook}")
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/check_webhook')
def check_webhook():
    """Проверка вебхука"""
    try:
        response = requests.get(f"{BASE_URL}/getWebhookInfo")
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/check_bot')
def check_bot():
    """Проверка бота"""
    try:
        response = requests.get(f"{BASE_URL}/getMe")
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/webhook', methods=['POST'])
def webhook():
    """Основной эндпоинт вебхука"""
    try:
        data = request.get_json()
        
        if 'message' in data:
            chat_id = data['message']['chat']['id']
            text = data['message'].get('text', '')
            
            # Простая логика ответа
            if text == '/start':
                send_message(chat_id, "🎉 Бот работает! Вебхук установлен на bothost!")
            elif text == '/domain':
                send_message(chat_id, f"Домен бота: {WEBHOOK_DOMAIN}")
            elif text:
                send_message(chat_id, f"Вы написали: {text}")
        
        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"ok": False, "error": str(e)}, 500

def send_message(chat_id, text):
    """Отправка сообщения"""
    try:
        response = requests.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            }
        )
        return response.json()
    except Exception as e:
        logger.error(f"Send message error: {e}")

if __name__ == '__main__':
    # Выводим информацию для отладки
    print("=" * 50)
    print("🤖 TELEGRAM BOT STARTUP")
    print("=" * 50)
    print(f"Token: {TOKEN[:10]}..." if TOKEN else "Token: NOT SET")
    print(f"Webhook URL: {WEBHOOK_URL}")
    
    # Проверяем токен
    if TOKEN:
        try:
            # Проверяем бота
            print("\n🔍 Checking bot...")
            bot_response = requests.get(f"{BASE_URL}/getMe").json()
            print(f"Bot info: {bot_response}")
            
            if bot_response.get('ok'):
                print(f"✅ Bot @{bot_response['result']['username']} is valid")
                
                # Устанавливаем вебхук
                print(f"\n🌐 Setting webhook to: {WEBHOOK_URL}")
                webhook_response = requests.get(f"{BASE_URL}/setWebhook?url={WEBHOOK_URL}").json()
                print(f"Webhook response: {webhook_response}")
            else:
                print(f"❌ Bot error: {bot_response.get('description')}")
                
        except Exception as e:
            print(f"⚠️ Error: {e}")
    
    else:
        print("❌ ERROR: TELEGRAM_TOKEN is not set!")
        print("Please set TELEGRAM_TOKEN environment variable in bothost")
    
    # Запуск сервера
    port = int(os.environ.get('PORT', 3000))
    print(f"\n🚀 Starting server on port {port}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
