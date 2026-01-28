import os
import logging
from flask import Flask, request, jsonify
import telebot
from telebot import types
import json
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация для вебхука
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DOMAIN = os.getenv('BOTHOST_DOMAIN', 'manualwebhookbothost.bothost.ru')
PORT = int(os.getenv('PORT', 8080))

# Проверка токена
if not TOKEN:
    logger.error("❌ ТОКЕН НЕ НАЙДЕН! Установите TELEGRAM_BOT_TOKEN в настройках Bot Host")
    raise ValueError("Токен бота не найден")

# Инициализация
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Глобальная переменная для отслеживания состояния вебхука
webhook_configured = False

def configure_webhook(force=False):
    """Настройка вебхука - ВЫЗЫВАЕТСЯ АВТОМАТИЧЕСКИ ПРИ ЗАПУСКЕ"""
    global webhook_configured
    
    if webhook_configured and not force:
        logger.info("Вебхук уже настроен")
        return True
    
    try:
        # Формируем URL вебхука
        webhook_url = f"https://{DOMAIN}/webhook"
        
        # Удаляем старый вебхук
        bot.remove_webhook()
        
        # Устанавливаем новый вебхук
        success = bot.set_webhook(
            url=webhook_url,
            max_connections=50,
            timeout=60
        )
        
        if success:
            webhook_configured = True
            logger.info(f"✅ ВЕБХУК УСПЕШНО УСТАНОВЛЕН!")
            logger.info(f"🌐 URL: {webhook_url}")
            
            # Получаем информацию о вебхуке
            webhook_info = bot.get_webhook_info()
            logger.info(f"📊 Информация о вебхуке: {webhook_info.to_dict()}")
            
            return True
        else:
            logger.error("❌ Не удалось установить вебхук")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка настройки вебхука: {e}")
        return False

# Конфигурируем вебхук ПРИ ЗАПУСКЕ приложения
configure_webhook()

# ============ ОБРАБОТЧИКИ КОМАНД ============

@bot.message_handler(commands=['start'])
def start_handler(message):
    """Обработка команды /start"""
    user = message.from_user
    
    welcome_text = f"""
    🎉 <b>ПРИВЕТ, {user.first_name}!</b>

    ✅ <b>Бот работает на вебхуках!</b>
    🌐 <b>Домен:</b> {DOMAIN}
    🆔 <b>Ваш ID:</b> <code>{user.id}</code>
    🤖 <b>Бот:</b> @{bot.get_me().username}

    <b>Команды:</b>
    /start - Начало работы
    /webhook - Проверить вебхук
    /status - Статус бота
    /echo [текст] - Эхо

    <b>Тестируйте команды!</b>
    """
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='HTML'
    )
    
    logger.info(f"Новый пользователь: {user.first_name} (ID: {user.id})")

@bot.message_handler(commands=['webhook'])
def webhook_info(message):
    """Информация о вебхуке"""
    try:
        info = bot.get_webhook_info().to_dict()
        
        status = "✅ АКТИВЕН" if info.get('url') else "❌ НЕ АКТИВЕН"
        
        response = f"""
        🌐 <b>ИНФОРМАЦИЯ О ВЕБХУКЕ</b>

        <b>Статус:</b> {status}
        <b>URL:</b> <code>{info.get('url', 'Не установлен')}</code>
        <b>Домен:</b> {DOMAIN}
        <b>Ожидающих сообщений:</b> {info.get('pending_update_count', 0)}
        <b>Макс. соединений:</b> {info.get('max_connections', 40)}
        
        <b>Для переустановки:</b>
        https://{DOMAIN}/set_webhook
        """
        
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")

@bot.message_handler(commands=['status'])
def status_command(message):
    """Статус бота"""
    status_text = f"""
    📊 <b>СТАТУС БОТА</b>

    ✅ <b>Работает на вебхуках</b>
    🌐 <b>Домен:</b> {DOMAIN}
    🤖 <b>Username:</b> @{bot.get_me().username}
    ⚡ <b>Режим:</b> Вебхук (Webhook)
    🔧 <b>Вебхук настроен:</b> {'Да' if webhook_configured else 'Нет'}
    
    <b>Health check:</b> https://{DOMAIN}/health
    <b>Инфо о вебхуке:</b> https://{DOMAIN}/webhook_info
    """
    
    bot.send_message(message.chat.id, status_text, parse_mode='HTML')

@bot.message_handler(commands=['echo'])
def echo_command(message):
    """Эхо команда"""
    text = message.text[6:] if len(message.text) > 6 else "Вы ничего не написали"
    bot.reply_to(message, f"🔊 Эхо: {text}")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    """Обработка всех сообщений"""
    bot.reply_to(message, f"📝 Вы написали: {message.text}")

# ============ FLASK ENDPOINTS ============

@app.route('/webhook', methods=['POST'])
def webhook():
    """Основной endpoint для вебхука Telegram"""
    if request.headers.get('content-type') == 'application/json':
        try:
            update = telebot.types.Update.de_json(request.get_json())
            bot.process_new_updates([update])
            logger.debug(f"Обработано обновление: {update.update_id}")
            return jsonify({'status': 'ok'}), 200
        except Exception as e:
            logger.error(f"Ошибка обработки вебхука: {e}")
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid content-type'}), 400

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook_endpoint():
    """Endpoint для установки вебхука (вручную)"""
    try:
        success = configure_webhook(force=True)
        
        if success:
            info = bot.get_webhook_info().to_dict()
            return jsonify({
                'status': 'success',
                'message': 'Вебхук успешно установлен',
                'domain': DOMAIN,
                'webhook_url': info.get('url'),
                'webhook_info': info
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Не удалось установить вебхук'
            }), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/remove_webhook', methods=['GET'])
def remove_webhook():
    """Удаление вебхука"""
    try:
        bot.remove_webhook()
        global webhook_configured
        webhook_configured = False
        
        return jsonify({
            'status': 'success',
            'message': 'Вебхук удален'
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check для Bot Host"""
    return jsonify({
        'status': 'healthy',
        'bot': bot.get_me().username if TOKEN else 'not_configured',
        'webhook_configured': webhook_configured,
        'domain': DOMAIN,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/webhook_info', methods=['GET'])
def get_webhook_info():
    """Получить информацию о вебхуке"""
    try:
        info = bot.get_webhook_info().to_dict()
        return jsonify({
            'status': 'success',
            'webhook_info': info,
            'domain': DOMAIN,
            'configured': webhook_configured
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def index():
    """Главная страница"""
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Telegram Bot на Webhook</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.95);
                color: #333;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h1 {{ color: #667eea; margin-top: 0; }}
            .status {{
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                font-weight: bold;
            }}
            .success {{ background: #d4edda; color: #155724; }}
            .endpoints {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            .endpoint {{
                background: white;
                padding: 15px;
                margin: 10px 0;
                border-left: 5px solid #667eea;
                border-radius: 5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .btn {{
                background: #667eea;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                display: inline-block;
                margin: 5px;
                transition: transform 0.2s;
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .instructions {{
                background: #e9ecef;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Bot на Bot Host</h1>
            <p><strong>Домен:</strong> {DOMAIN}</p>
            
            <div class="status success">
                ✅ Бот активен и работает на вебхуках
            </div>
            
            <div class="instructions">
                <h3>📋 Инструкция по настройке:</h3>
                <ol>
                    <li>Установите токен бота в настройках Bot Host: <code>TELEGRAM_BOT_TOKEN</code></li>
                    <li>Вебхук автоматически установится при запуске</li>
                    <li>Для проверки перейдите в Telegram и напишите боту</li>
                </ol>
            </div>
            
            <div class="endpoints">
                <h3>🔧 Доступные endpoints:</h3>
                
                <div class="endpoint">
                    <span><strong>GET /</strong> - Эта страница</span>
                    <a href="/" class="btn">Открыть</a>
                </div>
                
                <div class="endpoint">
                    <span><strong>POST /webhook</strong> - Webhook Telegram</span>
                    <code>используется ботом</code>
                </div>
                
                <div class="endpoint">
                    <span><strong>GET /set_webhook</strong> - Установить вебхук</span>
                    <a href="/set_webhook" class="btn">Установить</a>
                </div>
                
                <div class="endpoint">
                    <span><strong>GET /webhook_info</strong> - Информация о вебхуке</span>
                    <a href="/webhook_info" class="btn">Проверить</a>
                </div>
                
                <div class="endpoint">
                    <span><strong>GET /health</strong> - Health check</span>
                    <a href="/health" class="btn">Проверить</a>
                </div>
                
                <div class="endpoint">
                    <span><strong>GET /remove_webhook</strong> - Удалить вебхук</span>
                    <a href="/remove_webhook" class="btn">Удалить</a>
                </div>
            </div>
            
            <h3>🚀 Быстрый старт:</h3>
            <p>1. <a href="/set_webhook" class="btn">Активировать вебхук</a></p>
            <p>2. <a href="https://t.me/{bot.get_me().username}" target="_blank" class="btn">Открыть бота в Telegram</a></p>
            <p>3. Отправьте команду <code>/start</code></p>
        </div>
        
        <script>
            // Автоматически устанавливаем вебхук при загрузке страницы
            fetch('/set_webhook')
                .then(response => response.json())
                .then(data => {{
                    if(data.status === 'success') {{
                        console.log('✅ Вебхук установлен:', data.webhook_url);
                    }}
                }});
        </script>
    </body>
    </html>
    '''

# ============ ЗАПУСК ПРИЛОЖЕНИЯ ============

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info(f"🚀 ЗАПУСК БОТА НА ВЕБХУКАХ")
    logger.info(f"🌐 Домен: {DOMAIN}")
    logger.info(f"🤖 Бот: @{bot.get_me().username}")
    logger.info(f"🔧 Порт: {PORT}")
    logger.info("=" * 60)
    
    # Запускаем Flask приложение
    app.run(host='0.0.0.0', port=PORT, debug=False)
