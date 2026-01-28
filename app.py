import os
import logging
from flask import Flask, request
import telebot

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = f"https://{os.getenv('BOTHOST_DOMAIN', 'manualwebhookbothost.bothost.ru')}/webhook"

# Проверка токена
if not TOKEN:
    logger.error("❌ Токен не найден!")
    raise ValueError("Установите TELEGRAM_BOT_TOKEN в настройках Bot Host")

# Инициализация
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ============ ОБРАБОТЧИКИ КОМАНД ============

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Обработка /start и /help"""
    bot.reply_to(message, "✅ Бот работает на вебхуках!\nДомен: manualwebhookbothost.bothost.ru")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Эхо все сообщения"""
    bot.reply_to(message, f"Вы сказали: {message.text}")

# ============ ВЕБХУК ENDPOINTS ============

@app.route('/webhook', methods=['POST'])
def webhook():
    """Основной endpoint для вебхука"""
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 400

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка вебхука"""
    try:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL, max_connections=50)
        logger.info(f"✅ Вебхук установлен: {WEBHOOK_URL}")
        return f'✅ Вебхук установлен: {WEBHOOK_URL}', 200
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return f'❌ Ошибка: {e}', 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return {'status': 'healthy', 'bot': bot.get_me().username}, 200

@app.route('/')
def index():
    """Главная страница"""
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>🤖 Bot</title></head>
    <body>
        <h1>✅ Бот работает</h1>
        <p>Домен: manualwebhookbothost.bothost.ru</p>
        <p><a href="/set_webhook">Установить вебхук</a></p>
        <p><a href="/health">Health check</a></p>
    </body>
    </html>
    '''

# ============ АВТОМАТИЧЕСКАЯ УСТАНОВКА ВЕБХУКА ============

# Устанавливаем вебхук при импорте модуля
try:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL, max_connections=50)
    logger.info(f"🚀 Вебхук установлен автоматически: {WEBHOOK_URL}")
except Exception as e:
    logger.error(f"❌ Ошибка автоматической установки: {e}")

# Точка входа для Gunicorn
if __name__ == '__main__':
    # Этот код выполняется только при локальном запус
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080))) 
