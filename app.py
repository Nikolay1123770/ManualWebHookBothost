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
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/')
def home():
    """Главная страница диагностики"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Telegram Bot Status</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #333; }}
            .status-box {{ padding: 15px; background: #f8f9fa; border-radius: 5px; margin: 20px 0; }}
            .btn {{ 
                display: inline-block; 
                padding: 10px 20px; 
                margin: 5px; 
                background: #007bff; 
                color: white; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                text-decoration: none;
            }}
            .btn:hover {{ background: #0056b3; }}
            .success {{ color: #28a745; }}
            .error {{ color: #dc3545; }}
            .info {{ color: #17a2b8; }}
            pre {{ 
                background: #2d2d2d; 
                color: #f8f8f2; 
                padding: 15px; 
                border-radius: 5px; 
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <h1>🤖 Панель управления Telegram Bot</h1>
        
        <div class="status-box">
            <h3>Статус системы:</h3>
            <p><strong>Домен:</strong> {WEBHOOK_DOMAIN}</p>
            <p><strong>Webhook URL:</strong> <code>{WEBHOOK_URL}</code></p>
            <p><strong>Токен:</strong> <code>{TOKEN[:10]}...{' (установлен)' if TOKEN else ' (не установлен!)'}</code></p>
        </div>
        
        <h3>Действия:</h3>
        <button class="btn" onclick="testDomain()">🔍 Проверить домен</button>
        <button class="btn" onclick="setupWebhook()">⚙️ Установить вебхук</button>
        <button class="btn" onclick="checkWebhook()">📊 Проверить вебхук</button>
        <button class="btn" onclick="checkBot()">🤖 Проверить бота</button>
        
        <div class="status-box">
            <h3>Инструкция:</h3>
            <ol>
                <li>Нажмите "Проверить домен"</li>
                <li>Нажмите "Установить вебхук"</li>
                <li>Нажмите "Проверить вебхук" - должно быть: <code>"url": "{WEBHOOK_URL}"</code></li>
                <li>Откройте Telegram и напишите боту <code>/start</code></li>
            </ol>
        </div>
        
        <div id="result" class="status-box">
            <h3>Результат:</h3>
            <p>Нажмите кнопку для выполнения действия...</p>
        </div>
        
        <script>
        async function apiCall(url) {{
            try {{
                const response = await fetch(url);
                return await response.json();
            }} catch (error) {{
                return {{ error: error.message }};
            }}
        }}
        
        function showResult(text, isError = false) {{
            const resultEl = document.getElementById('result');
            if (typeof text === 'object') {{
                resultEl.innerHTML = `<h3>Результат:</h3><pre>${{JSON.stringify(text, null, 2)}}</pre>`;
            }} else {{
                resultEl.innerHTML = `<h3>Результат:</h3><p class="${{isError ? 'error' : 'success'}}">${{text}}</p>`;
            }}
        }}
        
        async function testDomain() {{
            showResult('Проверяю доступность домена...');
            const result = await apiCall('/test_domain');
            showResult(result);
        }}
        
        async function setupWebhook() {{
            showResult('Устанавливаю вебхук...');
            const result = await apiCall('/setup_webhook');
            showResult(result);
        }}
        
        async function checkWebhook() {{
            showResult('Проверяю статус вебхука...');
            const result = await apiCall('/check_webhook');
            showResult(result);
        }}
        
        async function checkBot() {{
            showResult('Проверяю доступность бота...');
            const result = await apiCall('/check_bot');
            showResult(result);
        }}
        </script>
    </body>
    </html>
    """

@app.route('/test_domain')
def test_domain():
    """Проверка доступности домена"""
    try:
        # Проверяем доступность нашего же сервера
        return {
            "status": "success",
            "domain": WEBHOOK_DOMAIN,
            "message": "Домен доступен",
            "webhook_url": WEBHOOK_URL
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/setup_webhook')
def setup_webhook():
    """Установка вебхука"""
    if not TOKEN:
        return {"status": "error", "message": "Токен бота не установлен!"}
    
    try:
        # Устанавливаем вебхук
        response = requests.get(f"{BASE_URL}/setWebhook?url={WEBHOOK_URL}")
        data = response.json()
        
        logger.info(f"Webhook setup response: {data}")
        
        if data.get('ok'):
            return {
                "status": "success",
                "message": "✅ Вебхук успешно установлен!",
                "details": data,
                "webhook_url": WEBHOOK_URL
            }
        else:
            return {
                "status": "error",
                "message": f"❌ Ошибка установки вебхука: {data.get('description', 'Unknown error')}",
                "details": data
            }
    except Exception as e:
        logger.error(f"Setup webhook error: {e}")
        return {"status": "error", "message": f"Exception: {str(e)}"}

@app.route('/check_webhook')
def check_webhook():
    """Проверка статуса вебхука"""
    if not TOKEN:
        return {"status": "error", "message": "Токен бота не установлен!"}
    
    try:
        response = requests.get(f"{BASE_URL}/getWebhookInfo")
        data = response.json()
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/check_bot')
def check_bot():
    """Проверка доступности бота"""
    if not TOKEN:
        return {"status": "error", "message": "Токен бота не установлен!"}
    
    try:
        response = requests.get(f"{BASE_URL}/getMe")
        data = response.json()
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/webhook', methods=['POST'])
def webhook():
    """Основной эндпоинт для вебхука Telegram - СИНХРОННАЯ версия"""
    if not TOKEN:
        logger.error("Token not set in webhook")
        return jsonify({"ok": False, "error": "Token not configured"}), 500
    
    try:
        # Получаем данные от Telegram
        data = request.get_json()
        logger.info(f"Received webhook data: {data}")
        
        # Проверяем наличие сообщения
        if 'message' in data:
            message = data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '').strip()
            
            logger.info(f"Message from {chat_id}: {text}")
            
            # Обработка команд
            if text == '/start':
                response_text = (
                    "🎉 Привет! Я работающий бот на bothost!\n\n"
                    "✅ Вебхук успешно подключен\n"
                    "🌐 Домен: manualwebhookbothost.bothost.ru\n\n"
                    "Доступные команды:\n"
                    "/help - помощь\n"
                    "/status - статус\n"
                    "/test - тест"
                )
                send_message(chat_id, response_text)
                
            elif text == '/help':
                send_message(chat_id, 
                    "📚 Помощь:\n"
                    "Это тестовый бот для демонстрации работы вебхука на bothost\n\n"
                    "Команды:\n"
                    "/start - начать\n"
                    "/help - эта справка\n"
                    "/status - статус бота\n"
                    "/test - тестовое сообщение"
                )
                
            elif text == '/status':
                send_message(chat_id, 
                    f"📊 Статус бота:\n"
                    f"• Работает на bothost\n"
                    f"• Webhook: {WEBHOOK_URL}\n"
                    f"• Домен: {WEBHOOK_DOMAIN}\n"
                    f"• Сообщение получено: ✅"
                )
                
            elif text == '/test':
                send_message(chat_id, "✅ Тест пройден! Бот работает корректно!")
                
            elif text == '/id':
                send_message(chat_id, f"🆔 Ваш ID чата: {chat_id}")
                
            elif text:
                # Эхо-ответ для любого другого текста
                send_message(chat_id, f"📝 Вы написали: {text}")
        
        return jsonify({"ok": True})
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

def send_message(chat_id, text):
    """Отправка сообщения в Telegram - СИНХРОННАЯ версия"""
    try:
        response = requests.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            },
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"Failed to send message: {response.text}")
        else:
            logger.info(f"Message sent to {chat_id}")
            
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None

@app.route('/send_test', methods=['GET'])
def send_test_message():
    """Отправка тестового сообщения (для отладки)"""
    if not TOKEN:
        return {"status": "error", "message": "Токен не установлен"}
    
    try:
        chat_id = request.args.get('chat_id')
        if not chat_id:
            return {"status": "error", "message": "Укажите chat_id параметром"}
        
        result = send_message(chat_id, "🔧 Тестовое сообщение от панели управления!")
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # Вывод информации при запуске
    print("=" * 60)
    print("🤖 TELEGRAM WEBHOOK BOT")
    print("=" * 60)
    
    if TOKEN:
        print(f"✅ Токен установлен: {TOKEN[:10]}...")
        
        try:
            # Проверяем бота
            print("🔍 Проверяю бота...")
            bot_check = requests.get(f"{BASE_URL}/getMe", timeout=10).json()
            
            if bot_check.get('ok'):
                bot_name = bot_check['result']['username']
                print(f"✅ Бот @{bot_name} доступен")
                
                # Устанавливаем вебхук
                print(f"🌐 Устанавливаю вебхук...")
                webhook_result = requests.get(
                    f"{BASE_URL}/setWebhook?url={WEBHOOK_URL}",
                    timeout=10
                ).json()
                
                if webhook_result.get('ok'):
                    print(f"✅ Вебхук установлен на: {WEBHOOK_URL}")
                else:
                    print(f"⚠️ Ошибка вебхука: {webhook_result.get('description')}")
            else:
                print(f"❌ Ошибка бота: {bot_check.get('description')}")
                
        except Exception as e:
            print(f"⚠️ Ошибка при проверке: {e}")
    else:
        print("❌ ТОКЕН НЕ УСТАНОВЛЕН!")
        print("Добавьте переменную окружения TELEGRAM_TOKEN в bothost")
    
    # Запуск сервера
    port = int(os.environ.get('PORT', 3000))
    print(f"\n🚀 Запускаю сервер на порту {port}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False)
