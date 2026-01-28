import os
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, Update
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

# ==================== КОНФИГУРАЦИЯ ====================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8506600032:AAE4YTWOjHrGdvDCg1nGgffMfFqGy4ur37M")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "").rstrip("/")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 3000))

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== ИНИЦИАЛИЗАЦИЯ БОТА ====================

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# ==================== КЛАВИАТУРЫ ====================

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Меню"), KeyboardButton(text="ℹ️ Инфо")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="📞 Контакты")]
        ],
        resize_keyboard=True
    )

def inline_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="no")
            ],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
        ]
    )

# ==================== FSM ====================

class UserForm(StatesGroup):
    waiting_for_feedback = State()

# ==================== ОБРАБОТЧИКИ ====================

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
        "Я работаю на BotHost!",
        reply_markup=main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📚 <b>Доступные команды:</b>\n\n"
        "/start - Начать\n"
        "/help - Помощь\n"
        "/menu - Меню\n"
        "/feedback - Отзыв"
    )

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("📋 Выберите действие:", reply_markup=inline_menu())

@router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.set_state(UserForm.waiting_for_feedback)
    await message.answer("📝 Напишите ваш отзыв:")

@router.message(UserForm.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    logger.info(f"Отзыв от {message.from_user.id}: {message.text}")
    await state.clear()
    await message.answer("✅ Спасибо!", reply_markup=main_menu())

@router.message(F.text == "📋 Меню")
async def btn_menu(message: Message):
    await message.answer("📋 Меню:", reply_markup=inline_menu())

@router.message(F.text == "ℹ️ Инфо")
async def btn_info(message: Message):
    await message.answer("ℹ️ Бот v1.0 на BotHost")

@router.message(F.text == "⚙️ Настройки")
async def btn_settings(message: Message):
    await message.answer("⚙️ Настройки в разработке...")

@router.message(F.text == "📞 Контакты")
async def btn_contacts(message: Message):
    await message.answer("📞 Email: support@example.com")

@router.callback_query(F.data == "yes")
async def cb_yes(callback: CallbackQuery):
    await callback.answer("✅")
    await callback.message.edit_text("✅ Вы выбрали Да!")

@router.callback_query(F.data == "no")
async def cb_no(callback: CallbackQuery):
    await callback.answer("❌")
    await callback.message.edit_text("❌ Вы выбрали Нет!")

@router.callback_query(F.data == "back")
async def cb_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("📋 Меню:", reply_markup=inline_menu())

@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("📸 Фото получено!")

@router.message(F.text)
async def echo(message: Message):
    await message.answer(f"Вы написали: <i>{message.text}</i>")

# ==================== FASTAPI ====================

app = FastAPI(title="Telegram Bot", version="1.0")

@app.on_event("startup")
async def on_startup():
    """Запуск бота"""
    logger.info("=" * 50)
    logger.info("🚀 ЗАПУСК БОТА")
    logger.info(f"🔧 BOT_TOKEN: {'✅ Установлен' if BOT_TOKEN else '❌ Не установлен'}")
    logger.info(f"🔧 WEBHOOK_HOST: {WEBHOOK_HOST}")
    logger.info(f"🔧 WEBHOOK_URL: {WEBHOOK_URL}")
    logger.info(f"🔧 PORT: {PORT}")
    logger.info("=" * 50)
    
    # Регистрируем роутер
    dp.include_router(router)
    
    # Удаляем старый webhook
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🗑️ Старый webhook удалён")
    except Exception as e:
        logger.error(f"❌ Ошибка удаления webhook: {e}")
    
    # Устанавливаем новый webhook
    if WEBHOOK_URL and WEBHOOK_HOST:
        try:
            await bot.set_webhook(
                url=WEBHOOK_URL,
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"]
            )
            
            # Проверяем webhook
            info = await bot.get_webhook_info()
            logger.info(f"✅ Webhook установлен!")
            logger.info(f"📡 URL: {info.url}")
            logger.info(f"📊 Pending updates: {info.pending_update_count}")
            
            if info.last_error_message:
                logger.warning(f"⚠️ Last error: {info.last_error_message}")
        except Exception as e:
            logger.error(f"❌ Ошибка установки webhook: {e}")
    else:
        logger.error("❌ WEBHOOK_HOST или BOT_TOKEN не установлены!")

@app.on_event("shutdown")
async def on_shutdown():
    """Остановка бота"""
    logger.info("🛑 Остановка бота...")
    try:
        await bot.delete_webhook()
        await bot.session.close()
        logger.info("✅ Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка при остановке: {e}")

@app.get("/")
async def root():
    """Главная страница"""
    return {
        "status": "ok",
        "bot": "running",
        "webhook": WEBHOOK_URL,
        "message": "Bot is working!"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "healthy": True}

@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    """Обработка webhook от Telegram"""
    try:
        data = await request.json()
        logger.info(f"📨 Получен update: {data.get('update_id', 'unknown')}")
        
        update = Update(**data)
        await dp.feed_update(bot=bot, update=update)
        
        return JSONResponse(content={"ok": True})
    except Exception as e:
        logger.error(f"❌ Ошибка обработки webhook: {e}")
        return JSONResponse(content={"ok": True})  # Всё равно 200 для Telegram

# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    logger.info(f"🚀 Запуск сервера на порту {PORT}...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
