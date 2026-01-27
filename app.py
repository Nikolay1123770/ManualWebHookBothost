import os
import logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
import asyncio
from threading import Thread

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация Flask
app = Flask(__name__)

# Конфигурация
TOKEN = os.environ.get('TELEGRAM_TOKEN', 'ВАШ_ТОКЕН_БОТА')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://ваш-домен.bothost.app')
PORT = int(os.environ.get('PORT', 5000))

# Создание Application
application = Application.builder().token(TOKEN).build()

# Обработчики команд
async def start(update: Update, context):
    """Обработчик команды /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"🤖 Бот работает на вебхуке с bothost!\n"
        f"✅ Версия: python-telegram-bot 20.x\n"
        f"📡 Статус: Webhook активен"
    )

async def help_command(update: Update, context):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📚 Доступные команды:\n\n"
        "/start - Запуск бота\n"
        "/help - Справка\n"
        "/webhook - Информация о вебхуке\n"
        "/echo [текст] - Эхо\n\n"
        "Технологии:\n"
        "• Flask + python-telegram-bot 20.x\n"
        "• Webhook на bothost.app"
    )

async def echo(update: Update, context):
    """Эхо-ответ"""
    if context.args:
        text = ' '.join(context.args)
        await update.message.reply_text(f"📨 Вы сказали: {text}")
    else:
        await update.message.reply_text("Напишите текст после команды /echo")

async def webhook_info(update: Update, context):
    """Информация о вебхуке"""
    await update.message.reply_text(
        f"🌐 Информация о вебхуке:\n\n"
        f"URL: {WEBHOOK_URL}/webhook\n"
        f"Статус: ✅ Активен\n"
        f"Платформа: bothost.app\n"
        f"API версия: 20.x"
    )

async def handle_message(update: Update, context):
    """Обработка текстовых сообщений"""
    text = update.message.text
    await update.message.reply_text(f"Вы написали: {text}")

# Настройка обработчиков
def setup_handlers():
    """Добавление обработчиков"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("webhook", webhook_info))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask маршруты
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Telegram Bot Webhook</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .status { background: #4CAF50; color: white; padding: 15px; border-radius: 5px; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }
            code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🤖 Telegram Bot Webhook</h1>
        <div class="status">✅ Бот работает! Статус: Webhook активен</div>
        
        <h2>📊 Информация:</h2>
        <ul>
            <li><strong>Платформа:</strong> bothost.app</li>
            <li><strong>Метод:</strong> Webhook</li>
            <li><strong>Webhook URL:</strong> <code>{}/webhook</code></li>
            <li><strong>Библиотека:</strong> python-telegram-bot 20.x</li>
        </ul>
        
        <h2>🌐 Эндпоинты:</h2>
        <div class="endpoint"><strong>GET /</strong> - Эта страница</div>
        <div class="endpoint"><strong>POST /webhook</strong> - Вебхук от Telegram</div>
        <div class="endpoint"><strong>GET /set_webhook</strong> - Установить вебхук</div>
        
        <p>Проверьте бота в Telegram!</p>
    </body>
    </html>
    """.format(WEBHOOK_URL)

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Эндпоинт для вебхука"""
    try:
        data = request.get_json()
        update = Update.de_json(data, application.bot)
        
        # Обработка update
        await application.process_update(update)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"Ошибка в webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка вебхука"""
    try:
        # Запускаем асинхронную функцию
        async def _set_webhook():
            await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
        
        asyncio.run(_set_webhook())
        
        return jsonify({
            "status": "success",
            "message": f"Webhook установлен на {WEBHOOK_URL}/webhook",
            "url": f"{WEBHOOK_URL}/webhook"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    """Удаление вебхука"""
    try:
        async def _delete_webhook():
            await application.bot.delete_webhook()
        
        asyncio.run(_delete_webhook())
        
        return jsonify({
            "status": "success",
            "message": "Webhook удален"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "telegram-bot"})

def run_flask():
    """Запуск Flask приложения"""
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def main():
    """Основная функция запуска"""
    # Настройка обработчиков
    setup_handlers()
    
    # Запуск Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    logger.info(f"Бот запущен на порту {PORT}")
    logger.info(f"Webhook URL: {WEBHOOK_URL}/webhook")
    logger.info("Для установки вебхука перейдите на /set_webhook")

if __name__ == '__main__':
    main()
