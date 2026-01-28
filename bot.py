import os
import logging
import asyncio
from aiohttp import web

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import (
    Message, 
    CallbackQuery,
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# ==================== КОНФИГУРАЦИЯ ====================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8506600032:AAEwpmsVsssiog3gZNkRqZB3uXMNUGBEO2E")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "https://manualwebhookbothost.bothost.ru/webhook")  # https://your-bot.bothost.io
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" if WEBHOOK_HOST else None
PORT = int(os.getenv("PORT", 8080))

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Роутер
router = Router()

# ==================== КЛАВИАТУРЫ ====================

def main_menu() -> ReplyKeyboardMarkup:
    """Главное меню"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Меню"), KeyboardButton(text="ℹ️ Информация")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="📞 Контакты")],
            [KeyboardButton(text="📍 Отправить локацию", request_location=True)]
        ],
        resize_keyboard=True
    )

def inline_menu() -> InlineKeyboardMarkup:
    """Инлайн меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back"),
                InlineKeyboardButton(text="🏠 Домой", callback_data="home")
            ],
            [InlineKeyboardButton(text="🌐 Наш сайт", url="https://example.com")]
        ]
    )

def settings_menu() -> InlineKeyboardMarkup:
    """Меню настроек"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔔 Уведомления", callback_data="settings_notifications")],
            [InlineKeyboardButton(text="🌍 Язык", callback_data="settings_language")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
        ]
    )

# ==================== FSM СОСТОЯНИЯ ====================

class UserForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_feedback = State()

# ==================== КОМАНДЫ ====================

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
        f"Добро пожаловать в бота!\n"
        f"Используй меню ниже для навигации.",
        reply_markup=main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📚 <b>Список команд:</b>\n\n"
        "/start - Запустить бота\n"
        "/help - Показать помощь\n"
        "/menu - Открыть меню\n"
        "/feedback - Оставить отзыв\n"
        "/cancel - Отменить действие\n\n"
        "💡 <i>Также используйте кнопки меню!</i>"
    )

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "📋 <b>Главное меню</b>\n\nВыберите действие:",
        reply_markup=inline_menu()
    )

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Нечего отменять.")
        return
    await state.clear()
    await message.answer("✅ Действие отменено.", reply_markup=main_menu())

# ==================== FSM: FEEDBACK ====================

@router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.set_state(UserForm.waiting_for_feedback)
    await message.answer(
        "📝 Напишите ваш отзыв:\n\n"
        "<i>Для отмены: /cancel</i>"
    )

@router.message(UserForm.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    user = message.from_user
    logger.info(f"Feedback from {user.id} (@{user.username}): {message.text}")
    await state.clear()
    await message.answer(
        "✅ Спасибо за отзыв!",
        reply_markup=main_menu()
    )

# ==================== КНОПКИ REPLY ====================

@router.message(F.text == "📋 Меню")
async def btn_menu(message: Message):
    await message.answer(
        "📋 <b>Выберите раздел:</b>",
        reply_markup=inline_menu()
    )

@router.message(F.text == "ℹ️ Информация")
async def btn_info(message: Message):
    await message.answer(
        "ℹ️ <b>О боте</b>\n\n"
        "Версия: 1.0.0\n"
        "Разработчик: @your_username\n\n"
        "Бот на webhook для BotHost."
    )

@router.message(F.text == "⚙️ Настройки")
async def btn_settings(message: Message):
    await message.answer(
        "⚙️ <b>Настройки</b>\n\nВыберите параметр:",
        reply_markup=settings_menu()
    )

@router.message(F.text == "📞 Контакты")
async def btn_contacts(message: Message):
    await message.answer(
        "📞 <b>Контакты</b>\n\n"
        "📧 Email: example@mail.com\n"
        "📱 Telegram: @your_support\n"
        "🌐 Сайт: example.com"
    )

@router.message(F.location)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(
        f"📍 <b>Ваша локация:</b>\n\n"
        f"Широта: {lat}\n"
        f"Долгота: {lon}"
    )

# ==================== CALLBACK HANDLERS ====================

@router.callback_query(F.data == "confirm_yes")
async def callback_yes(callback: CallbackQuery):
    await callback.answer("✅ Вы выбрали Да!")
    await callback.message.edit_text("✅ Действие подтверждено.")

@router.callback_query(F.data == "confirm_no")
async def callback_no(callback: CallbackQuery):
    await callback.answer("❌ Вы выбрали Нет!")
    await callback.message.edit_text("❌ Действие отменено.")

@router.callback_query(F.data == "back")
async def callback_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📋 <b>Главное меню</b>",
        reply_markup=inline_menu()
    )

@router.callback_query(F.data == "home")
async def callback_home(callback: CallbackQuery):
    await callback.answer("🏠 Домой")
    await callback.message.delete()
    await callback.message.answer("🏠 Главная", reply_markup=main_menu())

@router.callback_query(F.data == "settings_notifications")
async def callback_notifications(callback: CallbackQuery):
    await callback.answer("🔔")
    await callback.message.edit_text(
        "🔔 <b>Уведомления</b>\n\n<i>В разработке...</i>",
        reply_markup=settings_menu()
    )

@router.callback_query(F.data == "settings_language")
async def callback_language(callback: CallbackQuery):
    await callback.answer("🌍")
    await callback.message.edit_text(
        "🌍 <b>Язык:</b> Русский 🇷🇺\n\n<i>В разработке...</i>",
        reply_markup=settings_menu()
    )

@router.callback_query(F.data == "back_to_main")
async def callback_back_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📋 <b>Главное меню</b>",
        reply_markup=inline_menu()
    )

# ==================== МЕДИА ====================

@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("📸 Красивое фото!")

@router.message(F.document)
async def handle_document(message: Message):
    await message.answer(f"📄 Файл: {message.document.file_name}")

@router.message(F.sticker)
async def handle_sticker(message: Message):
    await message.answer("👍 Классный стикер!")

@router.message(F.voice)
async def handle_voice(message: Message):
    await message.answer("🎤 Голосовое получено!")

# ==================== ЭХО ====================

@router.message(F.text)
async def echo(message: Message):
    await message.answer(
        f"🤖 Вы написали: <i>{message.text}</i>\n\n"
        f"Используйте /help для помощи."
    )

# ==================== WEBHOOK ====================

async def on_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    if WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
        logger.info(f"✅ Webhook: {WEBHOOK_URL}")
    else:
        logger.warning("⚠️ WEBHOOK_HOST не установлен!")

async def on_shutdown(bot: Bot):
    logger.info("🛑 Бот остановлен")
    await bot.delete_webhook()

async def health_check(request):
    return web.Response(text="OK", status=200)

# ==================== MAIN ====================

def main():
    # Создаём бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Диспетчер
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Веб-приложение
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    
    # Webhook handler
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    
    # Запуск
    logger.info(f"🚀 Запуск на порту {PORT}")
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
