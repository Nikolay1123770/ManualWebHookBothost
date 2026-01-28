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

# Получение переменных окружения (Bot Host автоматически устанавливает их)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Bot Host предоставляет URL вебхука
PORT = int(os.getenv('PORT', 8080))  # Bot Host использует порт 8080

# Проверка наличия обязательных переменных
if not TOKEN:
    logger.error("Токен бота не найден! Установите переменную TELEGRAM_BOT_TOKEN")
    raise ValueError("Токен бота не найден!")

# Инициализация бота и Flask приложения
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Глобальные переменные для хранения данных
# В реальном проекте используйте базу данных
user_sessions = {}

# Клавиатуры
def get_main_keyboard():
    """Основная клавиатура"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('📋 Информация')
    btn2 = types.KeyboardButton('⚙️ Настройки')
    btn3 = types.KeyboardButton('🆘 Помощь')
    btn4 = types.KeyboardButton('📊 Статистика')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def get_inline_keyboard():
    """Inline клавиатура"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Сайт', url='https://example.com')
    btn2 = types.InlineKeyboardButton('Документация', url='https://docs.example.com')
    btn3 = types.InlineKeyboardButton('Обновить', callback_data='refresh')
    btn4 = types.InlineKeyboardButton('Настройки', callback_data='settings')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# Обработчики команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработка команды /start"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Инициализация сессии пользователя
    user_sessions[user_id] = {
        'last_active': datetime.now().isoformat(),
        'command_count': 0
    }
    
    welcome_text = f"""
    👋 Привет, {user_name}!

    Я телеграм бот, развернутый на Bot Host.

    Доступные команды:
    /start - Начать работу
    /help - Получить помощь
    /info - Информация о боте
    /stats - Статистика использования
    /menu - Показать меню

    Выберите действие ниже или используйте команды.
    """
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode='HTML'
    )
    
    logger.info(f"Новый пользователь: {user_name} (ID: {user_id})")

@bot.message_handler(commands=['help'])
def send_help(message):
    """Обработка команды /help"""
    help_text = """
    🆘 <b>Помощь по боту</b>

    <b>Основные команды:</b>
    /start - Начало работы
    /help - Эта справка
    /info - Информация о боте
    /menu - Главное меню
    /stats - Статистика использования

    <b>Особенности:</b>
    • Бот работает 24/7 на Bot Host
    • Использует вебхуки для получения сообщений
    • Оптимизирован для облачного развертывания

    <b>Техническая поддержка:</b>
    По вопросам работы бота обращайтесь к администратору.
    """
    
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')
    logger.info(f"Пользователь {message.from_user.id} запросил помощь")

@bot.message_handler(commands=['info'])
def send_info(message):
    """Обработка команды /info"""
    info_text = f"""
    📊 <b>Информация о боте</b>

    <b>Текущий статус:</b> ✅ Активен
    <b>Платформа:</b> Bot Host
    <b>Режим:</b> Вебхук
    <b>Пользователей в сессии:</b> {len(user_sessions)}
    <b>ID вашего чата:</b> <code>{message.chat.id}</code>
    <b>Версия:</b> 1.0.0

    <b>Технологии:</b>
    • Python 3.9+
    • pyTelegramBotAPI
    • Flask
    • Bot Host инфраструктура
    """
    
    bot.send_message(message.chat.id, info_text, parse_mode='HTML')

@bot.message_handler(commands=['stats'])
def send_stats(message):
    """Обработка команды /stats"""
    user_id = message.from_user.id
    
    if user_id in user_sessions:
        user_stats = user_sessions[user_id]
        stats_text = f"""
        📈 <b>Ваша статистика</b>
        
        <b>Последняя активность:</b> {user_stats['last_active']}
        <b>Количество команд:</b> {user_stats['command_count']}
        <b>Общие сессии:</b> {len(user_sessions)}
        """
    else:
        stats_text = "Статистика не найдена. Используйте /start для начала работы."
    
    bot.send_message(message.chat.id, stats_text, parse_mode='HTML')
    user_sessions[user_id]['command_count'] += 1

@bot.message_handler(commands=['menu'])
def show_menu(message):
    """Показать меню"""
    bot.send_message(
        message.chat.id,
        "📱 <b>Главное меню</b>\n\nВыберите действие на клавиатуре:",
        reply_markup=get_main_keyboard(),
        parse_mode='HTML'
    )

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """Обработка всех текстовых сообщений"""
    user_id = message.from_user.id
    text = message.text.lower()
    
    # Обновление сессии пользователя
    if user_id not in user_sessions:
        user_sessions[user_id] = {'last_active': datetime.now().isoformat(), 'command_count': 0}
    else:
        user_sessions[user_id]['last_active'] = datetime.now().isoformat()
    
    # Обработка текстовых команд с клавиатуры
    if text == '📋 информация':
        bot.send_message(
            message.chat.id,
            "📋 <b>Информация</b>\n\nЭтот бот демонстрирует возможности развертывания на Bot Host.",
            parse_mode='HTML',
            reply_markup=get_inline_keyboard()
        )
    elif text == '⚙️ настройки':
        bot.send_message(
            message.chat.id,
            "⚙️ <b>Настройки</b>\n\nЗдесь будут доступны настройки бота.",
            parse_mode='HTML'
        )
    elif text == '🆘 помощь':
        send_help(message)
    elif text == '📊 статистика':
        send_stats(message)
    else:
        # Ответ на произвольное сообщение
        bot.send_message(
            message.chat.id,
            f"Вы сказали: {message.text}\n\nИспользуйте команды или меню для навигации.",
            reply_markup=get_main_keyboard()
        )
    
    logger.info(f"Получено сообщение от {user_id}: {message.text}")

# Обработка callback запросов от inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Обработка нажатий на inline кнопки"""
    if call.data == 'refresh':
        bot.answer_callback_query(call.id, "Обновление...")
        bot.edit_message_text(
            "✅ Данные обновлены!",
            call.message.chat.id,
            call.message.message_id
        )
    elif call.data == 'settings':
        bot.answer_callback_query(call.id, "Открываем настройки...")
        bot.send_message(call.message.chat.id, "Настройки открыты!")
    
    logger.info(f"Callback от {call.from_user.id}: {call.data}")

# Обработка ошибок
@bot.message_handler(func=lambda message: True, content_types=['audio', 'video', 'document', 'photo'])
def handle_media(message):
    """Обработка медиафайлов"""
    bot.send_message(
        message.chat.id,
        "📁 Я получил ваш файл! В текущей версии я фокусируюсь на текстовых командах.",
        reply_markup=get_main_keyboard()
    )

# Маршруты для вебхука
@app.route('/webhook', methods=['POST'])
def webhook():
    """Основной endpoint для вебхука"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Bad Request', 400

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка вебхука (вызывается при деплое)"""
    if not WEBHOOK_URL:
        return jsonify({'error': 'WEBHOOK_URL не установлен'}), 500
    
    webhook_url = f"{WEBHOOK_URL}/webhook"
    
    try:
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        logger.info(f"Вебхук установлен: {webhook_url}")
        return jsonify({
            'status': 'success',
            'message': f'Вебхук установлен на {webhook_url}',
            'webhook_info': bot.get_webhook_info().to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Ошибка установки вебхука: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/remove_webhook', methods=['GET'])
def remove_webhook():
    """Удаление вебхука"""
    try:
        bot.remove_webhook()
        logger.info("Вебхук удален")
        return jsonify({'status': 'success', 'message': 'Вебхук удален'}), 200
    except Exception as e:
        logger.error(f"Ошибка удаления вебхука: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint для Bot Host"""
    return jsonify({
        'status': 'healthy',
        'bot_username': bot.get_me().username if TOKEN else 'not_configured',
        'users_in_session': len(user_sessions),
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Главная страница"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot on Bot Host</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
            .healthy { background-color: #d4edda; color: #155724; }
            .endpoints { margin-top: 20px; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 4px solid #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Bot на Bot Host</h1>
            <p>Этот бот работает на вебхуках и оптимизирован для развертывания на Bot Host.</p>
            
            <div class="status healthy">
                ✅ Бот активен и готов к работе
            </div>
            
            <div class="endpoints">
                <h3>Доступные endpoints:</h3>
                <div class="endpoint"><strong>GET /</strong> - Эта страница</div>
                <div class="endpoint"><strong>POST /webhook</strong> - Webhook для Telegram</div>
                <div class="endpoint"><strong>GET /set_webhook</strong> - Установить вебхук</div>
                <div class="endpoint"><strong>GET /remove_webhook</strong> - Удалить вебхук</div>
                <div class="endpoint"><strong>GET /health</strong> - Health check</div>
            </div>
            
            <div style="margin-top: 30px;">
                <h3>Инструкция по деплою:</h3>
                <ol>
                    <li>Замените TELEGRAM_BOT_TOKEN на свой токен в Bot Host</li>
                    <li>Bot Host автоматически установит WEBHOOK_URL</li>
                    <li>После деплоя перейдите на /set_webhook для активации</li>
                    <li>Проверьте статус на /health</li>
                </ol>
            </div>
        </div>
    </body>
    </html>
    '''

# Точка входа для локального тестирования
if __name__ == '__main__':
    # В локальном режиме используем polling
    if os.environ.get('BOT_HOST_DEPLOY') is None:
        logger.info("Локальный режим: запуск polling...")
        bot.remove_webhook()
        bot.polling(none_stop=True)
    else:
        # В режиме Bot Host запускаем Flask приложение
        logger.info(f"Запуск на Bot Host на порту {PORT}")
        app.run(host='0.0.0.0', port=PORT, debug=False)
