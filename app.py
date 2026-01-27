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

# Конфигурация - ВАЖНО: замените на ваш токен!
TOKEN = os.environ.get('TELEGRAM_TOKEN', '8506600032:AAEGyei4Il9al_dcCnLOxcZDsrT6M8NgeIA')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Домен bothost - он уже правильный!
WEBHOOK_URL = "https://manualwebhookbothost.bothost.app/webhook"

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot Status</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .success { color: green; }
            .error { color: red; }
            button { padding: 10px 20px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>🤖 Telegram Bot Control Panel</h1>
        
        <div id="status">Проверяем статус...</div>
        
        <button onclick="setupWebhook()">1. Установить вебхук</button>
        <button onclick="checkWebhook()">2. Проверить вебхук</button>
        <button onclick="checkBot()">3. Проверить бота</button>
        <button onclick="sendTest()">4. Отправить тест в Telegram</button>
        
        <div id="result" style="margin-top: 20px; padding: 10px; background: #f0f0f0;"></div>
        
        <script>
        async function apiCall(endpoint) {
            const response = await fetch(endpoint);
            const data = await response.json();
            return data;
        }
        
        async function setupWebhook() {
            const result = document.getElementById('result');
            result.innerHTML = 'Устанавливаю вебхук...';
            
            try {
                const response = await fetch('/setup_webhook');
                const data = await response.json();
                result.innerHTML = JSON.stringify(data, null, 2);
            } catch (error) {
                result.innerHTML = 'Ошибка: ' + error;
            }
        }
        
        async function checkWebhook() {
            const result = document.getElementById('result');
            result.innerHTML = 'Проверяю вебхук...';
            
            try {
                const response = await fetch('/check_webhook');
                const data = await response.json();
                result.innerHTML = JSON.stringify(data, null, 2);
            } catch (error) {
                result.innerHTML = 'Ошибка: ' + error;
            }
        }
        
        async function checkBot() {
            const result = document.getElementById('result');
            result.innerHTML = 'Проверяю бота...';
            
            try {
                const response = await fetch('/check_bot');
                const data = await response.json();
                result.innerHTML = JSON.stringify(data, null, 2);
            } catch (error) {
                result.innerHTML = 'Ошибка: ' + error;
            }
        }
        
        async function sendTest() {
            const chatId = prompt('Введите ваш chat ID (напишите боту /id чтобы получить):');
            if (!chatId) return;
            
            const result = document.getElementById('result');
            result.innerHTML = 'Отправляю сообщение...';
            
            try {
                const response = await fetch(`/send_test?chat_id=${chatId}`);
                const data = await response.json();
                result.innerHTML = JSON.stringify(data, null, 2);
            } catch (error) {
                result.innerHTML = 'Ошибка: ' + error;
            }
        }
        
        // Проверяем статус при загрузке
        window.onload = function() {
            checkStatus();
        }
        
        async function checkStatus() {
            const status = document.getElementById('status');
            try {
                const response = await fetch('/status');
                const data = await response.json();
                status.innerHTML = `<span class="success">✅ ${data.message}</span>`;
            } catch (error) {
                status.innerHTML = `<span class="error">❌ Ошибка подключения</span>`;
            }
        }
        </script>
    </body>
    </html>
    """

@app.route('/status')
def status():
    return {"status": "online", "message": "Сервер работает!", "webhook_url": WEBHOOK_URL}

@app.route('/setup_webhook')
def setup_webhook():
    """Установка вебхука"""
    try:
        # Устанавливаем вебхук
        response = requests.get(f"{BASE_URL}/setWebhook?url={WEBHOOK_URL}")
        data = response.json()
        
        logger.info(f"Webhook setup result: {data}")
        
        # Проверяем установку
        if data.get('ok'):
            return {
                "status": "success",
                "message": "Вебхук успешно установлен!",
                "details": data,
                "webhook_url": WEBHOOK_URL
            }
        else:
            return {
                "status": "error",
                "message": f"Ошибка установки вебхука: {data.get('description', 'Unknown error')}",
                "details": data
            }
    except Exception as e:
        return {"status": "error", "message": f"Exception: {str(e)}"}

@app.route('/check_webhook')
def check_webhook():
    """Проверка вебхука"""
    try:
        response = requests.get(f"{BASE_URL}/getWebhookInfo")
        data = response.json()
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/check_bot')
def check_bot():
    """Проверка доступности бота"""
    try:
        response = requests.get(f"{BASE_URL}/getMe")
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/send_test')
def send_test():
    """Отправка тестового сообщения"""
    try:
        chat_id = request.args.get('chat_id')
        if not chat_id:
            return {"status": "error", "message": "Нет chat_id"}
        
        # Отправляем сообщение
        response = requests.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "✅ Тестовое сообщение от бота! Если вы видите это, бот работает!"
            }
        )
        
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/webhook', methods=['POST'])
def webhook():
    """Основной эндпоинт для вебхука Telegram"""
    try:
        data = request.get_json()
        logger.info(f"Received webhook data: {data}")
        
        # Обрабатываем сообщение
        if 'message' in data:
            message = data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '').strip()
            
            logger.info(f"Message from {chat_id}: {text}")
            
            # Обработка команд
            if text == '/start':
                send_message(chat_id, 
                    "🎉 Привет! Я бот на bothost!\n\n"
                    "Доступные команды:\n"
                    "/help - помощь\n"
                    "/id - получить ваш ID\n"
                    "/test - тестовая команда"
                )
            elif text == '/help':
                send_message(chat_id, 
                    "📚 Помощь:\n"
                    "Бот работает на платформе bothost\n"
                    "Использует webhook для получения сообщений\n"
                    "Код открыт и доступен на GitHub"
                )
            elif text == '/id':
                send_message(chat_id, f"🆔 Ваш chat ID: {chat_id}")
            elif text == '/test':
                send_message(chat_id, "✅ Тест пройден! Бот работает корректно!")
            elif text:
                send_message(chat_id, f"📝 Вы написали: {text}")
        
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

# Автоматически устанавливаем вебхук при запуске
if __name__ == '__main__':
    try:
        # Проверяем токен
        print(f"🔑 Токен: {TOKEN[:10]}...")
        
        # Устанавливаем вебхук
        print(f"🌐 Устанавливаю вебхук на: {WEBHOOK_URL}")
        response = requests.get(f"{BASE_URL}/setWebhook?url={WEBHOOK_URL}")
        print(f"📡 Результат установки вебхука: {response.json()}")
        
        # Проверяем бота
        print("🤖 Проверяю бота...")
        bot_info = requests.get(f"{BASE_URL}/getMe").json()
        print(f"📊 Информация о боте: {bot_info}")
        
        if bot_info.get('ok'):
            print(f"✅ Бот @{bot_info['result']['username']} готов к работе!")
        else:
            print(f"❌ Ошибка бота: {bot_info.get('description')}")
            
    except Exception as e:
        print(f"⚠️ Ошибка при запуске: {e}")
    
    # Запускаем сервер
    port = int(os.environ.get('PORT', 3000))
    print(f"🚀 Сервер запущен на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
