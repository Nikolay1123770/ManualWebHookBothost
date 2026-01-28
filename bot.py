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
bot_username = ""

def webhook_info_to_dict(webhook_info):
    """Конвертация объекта WebhookInfo в словарь"""
    return {
        'url': webhook_info.url,
        'has_custom_certificate': webhook_info.has_custom_certificate,
        'pending_update_count': webhook_info.pending_update_count,
        'max_connections': webhook_info.max_connections,
        'ip_address': webhook_info.ip_address
    }

def configure_webhook(force=False):
    """Настройка вебхука - ВЫЗЫВАЕТСЯ АВТОМАТИЧЕСКИ ПРИ ЗАПУСКЕ"""
    global webhook_configured, bot_username
    
    if webhook_configured and not force:
        logger.info("Вебхук уже настроен")
        return True
    
    try:
        # Получаем информацию о боте
        bot_info = bot.get_me()
        bot_username = bot_info.username
        
        # Формируем URL вебхука
        webhook_url = f"https://{DOMAIN}/webhook"
        
        logger.info(f"🔄 Настраиваю вебхук для бота @{bot_username}...")
        
        # Удаляем старый вебхук
        bot.remove_webhook()
        logger.info("Старый вебхук удален")
        
        # Устанавливаем новый вебхук
        success = bot.set_webhook(
            url=webhook_url,
            max_connections=50,
            timeout=60
        )
        
        if success:
            webhook_configured = True
            
            # Получаем информацию о вебхуке
            webhook_info = bot.get_webhook_info()
            webhook_dict = webhook_info_to_dict(webhook_info)
            
            logger.info("✅ ВЕБХУК УСПЕШНО УСТАНОВЛЕН!")
            logger.info(f"🌐 URL: {webhook_url}")
            logger.info(f"📊 Информация о вебхуке:")
            logger.info(f"   - URL: {webhook_dict['url']}")
            logger.info(f"   - Ожидающих обновлений: {webhook_dict['pending_update_count']}")
            logger.info(f"   - Макс. соединений: {webhook_dict['max_connections']}")
            logger.info(f"   - IP адрес: {webhook_dict['ip_address']}")
            
            return True
        else:
            logger.error("❌ Не удалось установить вебхук")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка настройки вебхука: {str(e)}")
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
    🤖 <b>Бот:</b> @{bot_username}

    <b>Команды:</b>
    /start - Начало работы
    /webhook - Проверить вебхук
    /status - Статус бота
    /echo [текст] - Эхо
    /test - Тест бота

    <b>Тестируйте команды!</b>
    """
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='HTML'
    )
    
    logger.info(f"📨 Команда /start от {user.first_name} (ID: {user.id})")

@bot.message_handler(commands=['test'])
def test_handler(message):
    """Тестовая команда"""
    bot.reply_to(message, "✅ Бот работает отлично! Вебхук активен.")

@bot.message_handler(commands=['webhook'])
def webhook_info(message):
    """Информация о вебхуке"""
    try:
        webhook_info = bot.get_webhook_info()
        info = webhook_info_to_dict(webhook_info)
        
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
    🤖 <b>Username:</b> @{bot_username}
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
    logger.info(f"📝 Сообщение от {message.from_user.id}: {message.text}")
    bot.reply_to(message, f"📝 Вы написали: {message.text}")

# ============ FLASK ENDPOINTS ============

@app.route('/webhook', methods=['POST'])
def webhook():
    """Основной endpoint для вебхука Telegram"""
    if request.headers.get('content-type') == 'application/json':
        try:
            update = telebot.types.Update.de_json(request.get_json())
            bot.process_new_updates([update])
            logger.debug(f"✅ Обработано обновление: {update.update_id}")
            return jsonify({'status': 'ok'}), 200
        except Exception as e:
            logger.error(f"❌ Ошибка обработки вебхука: {str(e)}")
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid content-type'}), 400

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook_endpoint():
    """Endpoint для установки вебхука (вручную)"""
    try:
        success = configure_webhook(force=True)
        
        if success:
            webhook_info_obj = bot.get_webhook_info()
            info = webhook_info_to_dict(webhook_info_obj)
            
            return jsonify({
                'status': 'success',
                'message': 'Вебхук успешно установлен',
                'domain': DOMAIN,
                'bot_username': bot_username,
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
            'message': 'Вебхук удален',
            'bot_username': bot_username
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check для Bot Host"""
    try:
        bot_info = bot.get_me()
        webhook_info_obj = bot.get_webhook_info()
        webhook_info = webhook_info_to_dict(webhook_info_obj)
        
        return jsonify({
            'status': 'healthy',
            'bot': bot_info.username,
            'bot_id': bot_info.id,
            'webhook_configured': webhook_configured,
            'webhook_url': webhook_info.get('url'),
            'domain': DOMAIN,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/webhook_info', methods=['GET'])
def get_webhook_info():
    """Получить информацию о вебхуке"""
    try:
        webhook_info_obj = bot.get_webhook_info()
        info = webhook_info_to_dict(webhook_info_obj)
        
        return jsonify({
            'status': 'success',
            'bot_username': bot_username,
            'webhook_info': info,
            'domain': DOMAIN,
            'configured': webhook_configured
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/bot_info', methods=['GET'])
def get_bot_info():
    """Получить информацию о боте"""
    try:
        bot_info = bot.get_me()
        
        return jsonify({
            'status': 'success',
            'bot_info': {
                'id': bot_info.id,
                'username': bot_info.username,
                'first_name': bot_info.first_name,
                'is_bot': bot_info.is_bot
            },
            'webhook_configured': webhook_configured,
            'domain': DOMAIN
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def index():
    """Главная страница"""
    webhook_status = "✅ АКТИВЕН" if webhook_configured else "❌ НЕ АКТИВЕН"
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Telegram Bot @{bot_username}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                color: #fff;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 24px;
                padding: 40px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                color: #333;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            
            .bot-avatar {{
                width: 120px;
                height: 120px;
                background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                border-radius: 50%;
                margin: 0 auto 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 48px;
                color: white;
            }}
            
            h1 {{
                color: #2d3748;
                font-size: 36px;
                margin-bottom: 10px;
            }}
            
            .subtitle {{
                color: #4a5568;
                font-size: 18px;
                margin-bottom: 30px;
            }}
            
            .status-card {{
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                color: white;
                padding: 25px;
                border-radius: 16px;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 20px;
            }}
            
            .status-icon {{
                font-size: 48px;
            }}
            
            .status-content h3 {{
                font-size: 24px;
                margin-bottom: 5px;
            }}
            
            .endpoints-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .endpoint-card {{
                background: #f7fafc;
                border: 2px solid #e2e8f0;
                border-radius: 16px;
                padding: 25px;
                transition: all 0.3s ease;
            }}
            
            .endpoint-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                border-color: #4299e1;
            }}
            
            .endpoint-card h3 {{
                color: #2d3748;
                margin-bottom: 10px;
                font-size: 18px;
            }}
            
            .endpoint-card p {{
                color: #4a5568;
                margin-bottom: 15px;
                font-size: 14px;
            }}
            
            .endpoint-url {{
                background: #edf2f7;
                padding: 12px;
                border-radius: 8px;
                font-family: monospace;
                font-size: 14px;
                margin-bottom: 15px;
                word-break: break-all;
            }}
            
            .btn {{
                display: inline-block;
                background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                color: white;
                padding: 12px 24px;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 14px;
            }}
            
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(66, 153, 225, 0.3);
            }}
            
            .btn-success {{
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            }}
            
            .btn-danger {{
                background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
            }}
            
            .instructions {{
                background: #ebf8ff;
                border-left: 4px solid #4299e1;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
            }}
            
            .instructions h3 {{
                color: #2d3748;
                margin-bottom: 15px;
            }}
            
            .instructions ol {{
                padding-left: 20px;
            }}
            
            .instructions li {{
                margin-bottom: 10px;
                color: #4a5568;
            }}
            
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #e2e8f0;
                color: #718096;
                font-size: 14px;
            }}
            
            .telegram-link {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: #0088cc;
                color: white;
                padding: 12px 24px;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                margin-top: 20px;
            }}
            
            .telegram-link:hover {{
                background: #0077b5;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 20px;
                }}
                
                .endpoints-grid {{
                    grid-template-columns: 1fr;
                }}
                
                h1 {{
                    font-size: 28px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="bot-avatar">🤖</div>
                <h1>Telegram Bot @{bot_username}</h1>
                <p class="subtitle">Работает на вебхуках • Домен: {DOMAIN}</p>
            </div>
            
            <div class="status-card">
                <div class="status-icon">✅</div>
                <div class="status-content">
                    <h3>Бот активен и работает</h3>
                    <p>Статус вебхука: {webhook_status}</p>
                </div>
            </div>
            
            <div class="instructions">
                <h3>📋 Быстрая настройка:</h3>
                <ol>
                    <li>Нажмите "Установить вебхук" ниже</li>
                    <li>Перейдите в Telegram и найдите @{bot_username}</li>
                    <li>Отправьте команду /start для проверки</li>
                    <li>Используйте /webhook для проверки статуса</li>
                </ol>
            </div>
            
            <div class="endpoints-grid">
                <div class="endpoint-card">
                    <h3>🌐 Установить вебхук</h3>
                    <p>Активирует получение сообщений от Telegram</p>
                    <div class="endpoint-url">GET /set_webhook</div>
                    <a href="/set_webhook" class="btn btn-success">Установить вебхук</a>
                </div>
                
                <div class="endpoint-card">
                    <h3>📊 Информация о вебхуке</h3>
                    <p>Показывает текущую конфигурацию вебхука</p>
                    <div class="endpoint-url">GET /webhook_info</div>
                    <a href="/webhook_info" class="btn">Проверить статус</a>
                </div>
                
                <div class="endpoint-card">
                    <h3>❤️ Health Check</h3>
                    <p>Проверка работоспособности бота</p>
                    <div class="endpoint-url">GET /health</div>
                    <a href="/health" class="btn">Проверить здоровье</a>
                </div>
                
                <div class="endpoint-card">
                    <h3>🤖 Информация о боте</h3>
                    <p>Основная информация о Telegram боте</p>
                    <div class="endpoint-url">GET /bot_info</div>
                    <a href="/bot_info" class="btn">Информация о боте</a>
                </div>
                
                <div class="endpoint-card">
                    <h3>🗑️ Удалить вебхук</h3>
                    <p>Отключает получение сообщений (только для отладки)</p>
                    <div class="endpoint-url">GET /remove_webhook</div>
                    <a href="/remove_webhook" class="btn btn-danger">Удалить вебхук</a>
                </div>
                
                <div class="endpoint-card">
                    <h3>🔧 Webhook Endpoint</h3>
                    <p>Основной endpoint для Telegram API</p>
                    <div class="endpoint-url">POST /webhook</div>
                    <p><small>Используется Telegram для отправки сообщений</small></p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="https://t.me/{bot_username}" target="_blank" class="telegram-link">
                    <span>💬 Перейти к боту в Telegram</span>
                </a>
            </div>
            
            <div class="footer">
                <p>Bot Host • {DOMAIN} • Версия 1.0.0</p>
                <p>Все системы работают нормально ⚡</p>
            </div>
        </div>
        
        <script>
            // Автоматическая проверка статуса при загрузке
            async function checkStatus() {{
                try {{
                    const response = await fetch('/health');
                    const data = await response.json();
                    console.log('✅ Статус бота:', data);
                }} catch (error) {{
                    console.log('❌ Ошибка проверки статуса:', error);
                }}
            }}
            
            // Автоматически устанавливаем вебхук, если он не настроен
            async function autoSetupWebhook() {{
                try {{
                    const response = await fetch('/webhook_info');
                    const data = await response.json();
                    
                    if (data.status === 'success' && !data.webhook_info.url) {{
                        // Вебхук не установлен, устанавливаем автоматически
                        const setupResponse = await fetch('/set_webhook');
                        const setupData = await setupResponse.json();
                        
                        if (setupData.status === 'success') {{
                            console.log('✅ Вебхук автоматически установлен:', setupData.webhook_url);
                            alert('✅ Вебхук успешно установлен! Теперь бот готов к работе.');
                        }}
                    }}
                }} catch (error) {{
                    console.log('Автоматическая настройка не удалась:', error);
                }}
            }}
            
            // Запускаем проверки при загрузке страницы
            document.addEventListener('DOMContentLoaded', function() {{
                checkStatus();
                autoSetupWebhook();
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
    logger.info(f"🤖 Бот: @{bot_username}")
    logger.info(f"🔧 Порт: {PORT}")
    logger.info("=" * 60)
    
    # Запускаем Flask приложение
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
