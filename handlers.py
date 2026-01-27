import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from typing import List, Tuple

logger = logging.getLogger(__name__)

class BotHandlers:
    """Класс обработчиков команд бота"""
    
    @staticmethod
    def start(update: Update, context: CallbackContext) -> None:
        """Обработчик команды /start"""
        user = update.effective_user
        
        welcome_text = f"""
        👋 Привет, {user.first_name}!

        🤖 Я бот, работающий на вебхуках!
        📍 Использую bothost для хостинга
        ⚡ Быстрые ответы благодаря webhook
        
        Доступные команды:
        /help - Справка
        /menu - Меню с кнопками
        /webhook_info - Информация о вебхуке
        /echo [текст] - Эхо-ответ
        """
        
        update.message.reply_text(welcome_text)
        logger.info(f"Новый пользователь: {user.id} - {user.username}")
    
    @staticmethod
    def help_command(update: Update, context: CallbackContext) -> None:
        """Обработчик команды /help"""
        help_text = """
        📚 *Справочная информация*
        
        *Основные команды:*
        /start - Запуск бота
        /help - Эта справка
        /menu - Интерактивное меню
        /echo [текст] - Эхо
        /webhook_info - Инфо о вебхуке
        
        *Техническая информация:*
        • Бот работает на вебхуке
        • Хостинг: bothost.app
        • Используется Flask + python-telegram-bot
        
        *Исходный код:* [GitHub](https://github.com)
        """
        
        update.message.reply_text(help_text, parse_mode='Markdown')
    
    @staticmethod
    def menu(update: Update, context: CallbackContext) -> None:
        """Показ меню с инлайн-кнопками"""
        keyboard = [
            [
                InlineKeyboardButton("ℹ️ Информация", callback_data='info'),
                InlineKeyboardButton("🛠 Настройки", callback_data='settings')
            ],
            [
                InlineKeyboardButton("🔗 GitHub", url='https://github.com'),
                InlineKeyboardButton("📊 Статистика", callback_data='stats')
            ],
            [
                InlineKeyboardButton("❌ Закрыть", callback_data='close')
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            "📱 *Главное меню:*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    @staticmethod
    def button_handler(update: Update, context: CallbackContext) -> None:
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        query.answer()  # Ответить на callback
        
        data = query.data
        
        if data == 'info':
            query.edit_message_text(
                text="ℹ️ *Информация о боте:*\n\n"
                     "• Работает на вебхуке\n"
                     "• Хостинг: bothost.app\n"
                     "• Быстрые ответы\n"
                     "• Поддержка инлайн-кнопок",
                parse_mode='Markdown'
            )
        elif data == 'settings':
            query.edit_message_text(
                text="⚙️ *Настройки:*\n\n"
                     "Настройки временно недоступны",
                parse_mode='Markdown'
            )
        elif data == 'stats':
            query.edit_message_text(
                text="📊 *Статистика:*\n\n"
                     "Пользователей: 1\n"
                     "Сообщений: 10\n"
                     "Время работы: 24ч",
                parse_mode='Markdown'
            )
        elif data == 'close':
            query.delete_message()
    
    @staticmethod
    def echo(update: Update, context: CallbackContext) -> None:
        """Эхо-ответ"""
        if not context.args:
            update.message.reply_text(
                "Напишите текст после команды /echo\n"
                "Пример: `/echo Привет мир!`",
                parse_mode='Markdown'
            )
            return
        
        text = ' '.join(context.args)
        update.message.reply_text(f"📨 Вы сказали: *{text}*", parse_mode='Markdown')
    
    @staticmethod
    def webhook_info(update: Update, context: CallbackContext) -> None:
        """Информация о вебхуке"""
        from config import config
        
        info_text = f"""
        🌐 *Информация о вебхуке:*
        
        • Метод: Webhook
        • URL: `{config.WEBHOOK_URL}/webhook`
        • Статус: Активен ✅
        • Хостинг: bothost.app
        
        *Преимущества вебхука:*
        - Меньше задержка
        - Экономия ресурсов
        - Лучше масштабируется
        """
        
        update.message.reply_text(info_text, parse_mode='Markdown')
    
    @staticmethod
    def handle_message(update: Update, context: CallbackContext) -> None:
        """Обработка текстовых сообщений"""
        text = update.message.text
        
        response = f"""
        📝 *Вы написали:* {text}
        
        ID сообщения: `{update.message.message_id}`
        Время: `{update.message.date}`
        """
        
        update.message.reply_text(response, parse_mode='Markdown')
    
    @staticmethod
    def error_handler(update: Update, context: CallbackContext) -> None:
        """Обработчик ошибок"""
        logger.error(f"Ошибка: {context.error}")
        
        if update and update.effective_chat:
            try:
                update.effective_chat.send_message(
                    "❌ Произошла ошибка при обработке запроса. "
                    "Попробуйте еще раз позже."
                )
            except:
                pass