import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import (
    Message, 
    CallbackQuery,
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    Update
)
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# ==================== КОНФИГУРАЦИЯ ====================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8506600032:AAE4YTWOjHrGdvDCg1nGgffMfFqGy4ur37M")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "").rstrip("/")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" if WEBHOOK_HOST else None

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== БОТ И ДИСПЕТЧЕР ====================

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# ==================== КЛАВИАТУРЫ ====================

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Меню"), KeyboardButton(text="ℹ️ Информация")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="📞 Контакты")],
            [KeyboardButton(text="📍 Локация", request_location=True)]
        ],
        resize_keyboard=True
    )

def inline_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back"),
                InlineKeyboardButton(text="🏠 Домой", callback_data="home")
            ]
        ]
    )

def settings_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔔 Уведомления", callback_data="settings_notif")],
            [InlineKeyboardButton(text="🌍 Язык", callback_data="settings_lang")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
        ]
    )

# ==================== FSM ====================

class UserForm(StatesGroup):
    waiting_for_feedback = State()

# ==================== КОМАНДЫ ====================

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
        f"Добро пожаловать в бота!",
        reply_markup=main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📚 <b>Команды:</b>\n\n"
        "/start - Запуск\n"
        "/help - Помощь\n"
        "/menu - Меню\n"
        "/feedback - Отзыв\n"
        "/cancel - Отмена"
    )

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("📋 <b>Меню:</b>", reply_markup=inline_menu())

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Отменено.", reply_markup=main_menu())

@router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.set_state(UserForm.waiting_for_feedback)
    await message.answer("📝 Напишите отзыв (/cancel для отмены):")

@router.message(UserForm.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    logger.info(f"Feedback from {message.from_user.id}: {message.text}")
    await state.clear()
    await message.answer("✅ Спасибо за отзыв!", reply_markup=main_menu())

# ==================== КНОПКИ ====================

@router.message(F.text == "📋 Меню")
async def btn_menu(message: Message):
    await message.answer("📋 <b>Меню:</b>", reply_markup=inline_menu())

@router.message(F.text == "ℹ️ Информация")
async def btn_info(message: Message):
    await message.answer("ℹ️ <b>О боте</b>\n\nВерсия: 1.0.0")

@router.message(F.text == "⚙️ Настройки")
async def btn_settings(message: Message):
    await message.answer("⚙️ <b>Настройки:</b>", reply_markup=settings_menu())

@router.message(F.text == "📞 Контакты")
async def btn_contacts(message: Message):
    await message.answer("📞 <b>Контакты</b>\n\n📧 test@mail.com")

@router.message(F.location)
async def handle_location(message: Message):
    await message.answer(f"📍 Широта: {message.location.latitude}\nДолгота: {message.location.longitude}")

# ==================== CALLBACKS ====================

@router.callback_query(F.data == "confirm_yes")
async def cb_yes(callback: CallbackQuery):
    await callback.answer("✅")
    await callback.message.edit_text("✅ Подтверждено!")

@router.callback_query(F.data == "confirm_no")
async def cb_no(callback: CallbackQuery):
    await callback.answer("❌")
    await callback.message.edit_text("❌ Отменено!")

@router.callback_query(F.data == "back")
async def cb_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("📋 <b>Меню:</b>", reply_markup=inline_menu())

@router.callback_query(F.data == "home")
async def cb_home(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("🏠 Главная", reply_markup=main_menu())

@router.callback_query(F.data == "settings_notif")
async def cb_notif(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("🔔 <b>Уведомления</b>\n\n<i>В разработке</i>", reply_markup=settings_menu())

@router.callback_query(F.data == "settings_lang")
async def cb_lang(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("🌍 Язык: Русский 🇷🇺", reply_markup=settings_menu())

@router.callback_query(F.data == "back_to_main")
async def cb_back_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("📋 <b>Меню:</b>", reply_markup=inline_menu())

# ==================== МЕДИА ====================

@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("📸 Фото получено!")

@router.message(F.document)
async def handle_doc(message: Message):
    await message.answer(f"📄 Файл: {message.document.file_name}")

@router.message(F.text)
async def echo(message: Message):
    await message.answer(f"Вы: <i>{message.text}</i>\n\n/help - помощь")

# ==================== FASTAPI APP ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logger.info(f"🔧 WEBHOOK_URL: {WEBHOOK_URL}")
    
    if WEBHOOK_URL:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(
            url=WEBHOOK_URL,
            allowed_updates=["message", "callback_query"]
        )
        info = await bot.get_webhook_info()
        logger.info(f"✅ Webhook установлен: {info.url}")
    else:
        logger.error("❌ WEBHOOK_HOST не задан!")
    
    yield
    
    # SHUTDOWN
    logger.info("🛑 Остановка бота...")
    await bot.delete_webhook()
    await bot.session.close()

# Создаём FastAPI приложение
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Bot is running!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    """Обработка вебхука от Telegram"""
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot=bot, update=update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return Response(status_code=200)  # Всегда 200, чтобы Telegram не повторял
