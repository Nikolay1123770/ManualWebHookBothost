import logging
import sys
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import (
    Dispatcher,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    Updater
)

from config import config
from handlers import BotHandlers

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Инициализация Flask
app = Flask(__name__)

# Инициализация бота
bot = Updater(token=config.TELEGRAM_TOKEN, use_context=True).bot
dispatcher = Dispatcher(bot, None, workers=0)

def setup_dispatcher(dp):
    """Настройка диспетчера команд"""
    
    # Команды
    dp.add_handler(CommandHandler("start", BotHandlers.start))
    dp.add_handler(CommandHandler("help", BotHandlers.help_command))
    dp.add_handler(CommandHandler("menu", BotHandlers.menu))
    dp.add_handler(CommandHandler("echo", BotHandlers.echo))
    dp.add_handler(CommandHandler("webhook_info", BotHandlers.webhook_info))
    
    # Обработчики кнопок
    dp.add_handler(CallbackQueryHandler(BotHandlers.button_handler))
    
    # Обработчики сообщений
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, 
        BotHandlers.handle_message
    ))
    
    # Обработчик ошибок
    dp.add_error_handler(BotHandlers.error_handler)
    
    return dp

# Настройка диспетчера
dispatcher = setup_dispatcher(dispatcher)

@app.route('/')
def index():
    """Главная страница"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Telegram Webhook Bot</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 {
                text-align: center;
                font-size: 2.5em;
            }
            .status {
                padding: 15px;
                background: rgba(0, 255, 0, 0.2);
                border-radius: 10px;
                margin: 20px 0;
                text-align: center;
            }
            .endpoints {
                margin-top: 30px;
            }
            .endpoint {
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #4CAF50;
            }
            code {
                background: rgba(0, 0, 0, 0.3);
                padding: 2px 5px;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Webhook Bot</h1>
            
            <div class="status">
                ✅ Бот работает! Статус: <strong>Webhook активен</strong>
            </div>
            
            <h2>📊 Информация:</h2>
            <ul>
                <li><strong>Метод:</strong> Webhook</li>
                <li><strong>Хостинг:</strong> bothost.app</li>
                <li><strong>Framework:</strong> Flask + python-telegram-bot</li>
                <li><strong>Webhook URL:</strong> <code>{}/webhook</code></li>
            </ul>
            
            <div class="endpoints">
                <h2>🌐 Доступные эндпоинты:</h2>
                
                <div class="endpoint">
                    <strong>GET /</strong> - Эта страница
                </div>
                
                <div class="endpoint">
                    <strong>POST /webhook</strong> - Webhook от Telegram
                </div>
                
                <div class="endpoint">
                    <strong>GET /set_webhook</strong> - Установить вебхук
                </div>
                
                <div class="endpoint">
                    <strong>GET /delete_webhook</strong> - Удалить вебхук
                </div>
                
                <div class="endpoint">
                    <strong>GET /webhook_info</strong> - Информация о вебхуке
                </div>
            </div>
            
            <div style="margin-top: 40px; text-align: center;">
                <p>Бот готов к работе! Откройте Telegram и найдите бота.</p>
            </div>
        </div>
    </body>
    </html>
    """.format(config.WEBHOOK_URL)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Эндпоинт для вебхука от Telegram"""
    try:
        # Получаем обновление от Telegram
        update = Update.de_json(request.get_json(force=True), bot)
        
        # Передаем обновление в диспетчер
        dispatcher.process_update(update)
        
        logger.info(f"Обработано обновление: {update.update_id}")
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Ошибка в webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка вебхука"""
    try:
        webhook_url = f"{config.WEBHOOK_URL}/webhook"
        result = bot.set_webhook(webhook_url)
        
        if result:
            logger.info(f"Webhook установлен: {webhook_url}")
            return jsonify({
                "status": "success",
                "message": f"Webhook установлен на {webhook_url}",
                "url": webhook_url
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Не удалось установить webhook"
            }), 500
            
    except Exception as e:
        logger.error(f"Ошибка установки webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    """Удаление вебхука"""
    try:
        result = bot.delete_webhook()
        
        if result:
            logger.info("Webhook удален")
            return jsonify({
                "status": "success",
                "message": "Webhook удален"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Не удалось удалить webhook"
            }), 500
            
    except Exception as e:
        logger.error(f"Ошибка удаления webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/webhook_info', methods=['GET'])
def get_webhook_info():
    """Получение информации о вебхуке"""
    try:
        info = bot.get_webhook_info()
        
        return jsonify({
            "status": "success",
            "webhook_info": {
                "url": info.url,
                "has_custom_certificate": info.has_custom_certificate,
                "pending_update_count": info.pending_update_count,
                "last_error_date": info.last_error_date,
                "last_error_message": info.last_error_message,
                "max_connections": info.max_connections,
                "allowed_updates": info.allowed_updates
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка получения webhook info: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check для мониторинга"""
    return jsonify({
        "status": "healthy",
        "service": "telegram-bot-webhook",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    # Установка вебхука при запуске
    webhook_url = f"{config.WEBHOOK_URL}/webhook"
    bot.set_webhook(webhook_url)
    logger.info(f"Webhook установлен: {webhook_url}")
    
    # Запуск Flask приложения
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )