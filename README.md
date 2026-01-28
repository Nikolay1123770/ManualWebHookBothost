# 🤖 Telegram Bot на Webhook
# 📘 ПОЛНЫЙ МАНУАЛ: Создание Telegram бота на Webhook для BotHost

## 📑 Содержание
1. [Что нужно для начала](#что-нужно-для-начала)
2. [Шаг 1: Создание бота в Telegram](#шаг-1-создание-бота-в-telegram)
3. [Шаг 2: Создание GitHub репозитория](#шаг-2-создание-github-репозитория)
4. [Шаг 3: Создание файлов бота](#шаг-3-создание-файлов-бота)
5. [Шаг 4: Регистрация на BotHost](#шаг-4-регистрация-на-bothost)
6. [Шаг 5: Подключение к BotHost](#шаг-5-подключение-к-bothost)
7. [Шаг 6: Настройка переменных](#шаг-6-настройка-переменных)
8. [Шаг 7: Запуск и проверка](#шаг-7-запуск-и-проверка)
9. [Решение проблем](#решение-проблем)

---

## 🎯 Что нужно для начала

### Обязательно:
- ✅ Компьютер/ноутбук
- ✅ Интернет
- ✅ Аккаунт Telegram (на телефоне или в десктопной версии)
- ✅ Email для регистрации

### Необязательно (но полезно):
- 💡 Базовые знания работы с компьютером
- 💡 Понимание что такое файлы и папки
- 💡 Умение копировать/вставлять текст

---

## 🤖 Шаг 1: Создание бота в Telegram

### 1.1 Открываем BotFather

1. **Откройте Telegram** (на телефоне или компьютере)
2. **В поиске напишите:** `@BotFather`
3. **Нажмите на результат:** Должен быть синий чекмарк (галочка)
4. **Нажмите кнопку "START"** внизу

![BotFather выглядит так]
```
BotFather ✓
Официальный бот для создания других ботов
```

### 1.2 Создаём нового бота

5. **Отправьте команду:** `/newbot`
   - Просто напишите это в чат с BotFather
   - Нажмите "Отправить"

6. **BotFather спросит имя бота. Введите:**
   ```
   My Awesome Bot
   ```
   - Это имя увидят пользователи
   - Может быть любым, даже с пробелами
   - Можно на русском: `Мой Крутой Бот`

7. **BotFather спросит username. Введите:**
   ```
   my_awesome_bot
   ```
   - ОБЯЗАТЕЛЬНО должен заканчиваться на `bot`
   - Только английские буквы, цифры и подчеркивания
   - БЕЗ пробелов
   - Примеры: `super_bot`, `mytest_bot`, `cool123_bot`

8. **BotFather выдаст сообщение:**
   ```
   Done! Congratulations on your new bot...
   
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567
   
   For a description of the Bot API, see this page...
   ```

### 1.3 ВАЖНО: Сохраняем токен!

9. **Найдите строку с токеном:**
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567
   ```

10. **Скопируйте её:**
    - **На телефоне:** Нажмите и держите на токене → Копировать
    - **На компьютере:** Выделите мышкой → Ctrl+C (Cmd+C на Mac)

11. **Сохраните в блокнот/заметки:**
    - Откройте любой текстовый редактор
    - Вставьте токен (Ctrl+V)
    - Сохраните файл как `bot_token.txt`

> ⚠️ **ВАЖНО!** Этот токен - ключ к вашему боту. Не показывайте его никому!

### 1.4 Настраиваем бота (опционально)

12. **Добавим описание. Отправьте:**
    ```
    /setdescription
    ```
    
13. **Выберите вашего бота** (нажмите на него в списке)

14. **Введите описание:**
    ```
    Это мой первый бот на BotHost! 🚀
    ```

15. **Добавим фото бота. Отправьте:**
    ```
    /setuserpic
    ```
    
16. **Выберите вашего бота**

17. **Отправьте любое фото** (минимум 200x200 пикселей)

---

## 📁 Шаг 2: Создание GitHub репозитория

### 2.1 Регистрация на GitHub (если нет аккаунта)

1. **Перейдите на** [github.com](https://github.com)
2. **Нажмите "Sign up"** (Зарегистрироваться)
3. **Введите email** → нажмите Continue
4. **Придумайте пароль** → нажмите Continue
5. **Придумайте username** → нажмите Continue
6. **Решите капчу** (подтвердите что вы не робот)
7. **Подтвердите email** (откройте письмо и введите код)

### 2.2 Создание репозитория

8. **На главной странице GitHub нажмите:** зелёную кнопку **"New"** (слева вверху)
   - Или перейдите: [github.com/new](https://github.com/new)

9. **Заполните форму:**
   
   **Repository name** (Имя репозитория):
   ```
   my-telegram-bot
   ```
   - Только английские буквы, цифры, дефисы
   - БЕЗ пробелов
   
   **Description** (Описание, необязательно):
   ```
   My first Telegram bot on BotHost
   ```
   
   **Public/Private** (Публичный/Приватный):
   - Выберите **Public** (бесплатно)
   
   **Add a README file:**
   - ✅ Поставьте галочку
   
   **Add .gitignore:**
   - Выберите **Python** из списка
   
   **Choose a license:**
   - Можно пропустить или выбрать **MIT License**

10. **Нажмите зелёную кнопку:** **"Create repository"**

### 2.3 Откроется ваш новый репозиторий

Вы увидите адрес типа:
```
https://github.com/ваш_username/my-telegram-bot
```

**Сохраните этот адрес!** Он понадобится позже.

---

## 💻 Шаг 3: Создание файлов бота

### 3.1 Создаём файл bot.py

1. **В вашем репозитории нажмите:** **"Add file"** → **"Create new file"**

2. **В поле "Name your file" напишите:**
   ```
   bot.py
   ```

3. **В большое поле ниже вставьте этот код:**

```python
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

# Получаем данные из переменных окружения (их установим позже в BotHost)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "").rstrip("/")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 3000))

# Настройка логирования (записи действий бота)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# ==================== КЛАВИАТУРЫ ====================

def main_menu():
    """Главное меню бота"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Меню"), KeyboardButton(text="ℹ️ Информация")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="📞 Помощь")],
        ],
        resize_keyboard=True
    )

def inline_menu():
    """Инлайн меню с кнопками"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="no")
            ],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
        ]
    )

# ==================== FSM (Состояния) ====================

class UserForm(StatesGroup):
    """Состояния для многошагового диалога"""
    waiting_for_feedback = State()

# ==================== ОБРАБОТЧИКИ КОМАНД ====================

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start"""
    user_name = message.from_user.first_name
    await message.answer(
        f"👋 <b>Привет, {user_name}!</b>\n\n"
        f"🎉 Я работаю на BotHost!\n"
        f"Используй меню ниже для навигации.",
        reply_markup=main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработка команды /help"""
    await message.answer(
        "📚 <b>Доступные команды:</b>\n\n"
        "/start - Запустить бота\n"
        "/help - Показать эту справку\n"
        "/menu - Показать меню\n"
        "/feedback - Оставить отзыв\n"
        "/cancel - Отменить текущее действие\n\n"
        "💡 Также можно использовать кнопки меню!"
    )

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Обработка команды /menu"""
    await message.answer(
        "📋 <b>Главное меню</b>\n\nВыберите действие:",
        reply_markup=inline_menu()
    )

@router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    """Запуск режима обратной связи"""
    await state.set_state(UserForm.waiting_for_feedback)
    await message.answer(
        "📝 <b>Обратная связь</b>\n\n"
        "Напишите ваш отзыв или предложение.\n"
        "Для отмены используйте /cancel"
    )

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Отмена текущего действия"""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Нечего отменять.")
        return
    
    await state.clear()
    await message.answer("✅ Действие отменено.", reply_markup=main_menu())

# ==================== ОБРАБОТКА СОСТОЯНИЙ ====================

@router.message(UserForm.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    """Получение отзыва от пользователя"""
    feedback_text = message.text
    user_id = message.from_user.id
    username = message.from_user.username or "без username"
    
    # Логируем отзыв
    logger.info(f"📝 Отзыв от {user_id} (@{username}): {feedback_text}")
    
    await state.clear()
    await message.answer(
        "✅ <b>Спасибо за ваш отзыв!</b>\n\n"
        "Мы обязательно его рассмотрим.",
        reply_markup=main_menu()
    )

# ==================== ОБРАБОТЧИКИ КНОПОК ====================

@router.message(F.text == "📋 Меню")
async def btn_menu(message: Message):
    """Кнопка Меню"""
    await message.answer("📋 <b>Меню</b>", reply_markup=inline_menu())

@router.message(F.text == "ℹ️ Информация")
async def btn_info(message: Message):
    """Кнопка Информация"""
    await message.answer(
        "ℹ️ <b>О боте</b>\n\n"
        "🤖 Версия: 1.0.0\n"
        "🚀 Платформа: BotHost\n"
        "💻 Технологии: Python, aiogram, FastAPI\n"
        "📅 Создан: 2026"
    )

@router.message(F.text == "⚙️ Настройки")
async def btn_settings(message: Message):
    """Кнопка Настройки"""
    await message.answer(
        "⚙️ <b>Настройки</b>\n\n"
        "Функция в разработке...\n"
        "Скоро здесь появятся настройки!"
    )

@router.message(F.text == "📞 Помощь")
async def btn_help(message: Message):
    """Кнопка Помощь"""
    await message.answer(
        "📞 <b>Нужна помощь?</b>\n\n"
        "📧 Email: support@example.com\n"
        "💬 Telegram: @your_support\n\n"
        "Или используйте /feedback для отправки сообщения!"
    )

# ==================== CALLBACK ОБРАБОТЧИКИ ====================

@router.callback_query(F.data == "yes")
async def callback_yes(callback: CallbackQuery):
    """Нажатие кнопки Да"""
    await callback.answer("✅ Вы выбрали Да!")
    await callback.message.edit_text("✅ <b>Вы выбрали: Да</b>")

@router.callback_query(F.data == "no")
async def callback_no(callback: CallbackQuery):
    """Нажатие кнопки Нет"""
    await callback.answer("❌ Вы выбрали Нет!")
    await callback.message.edit_text("❌ <b>Вы выбрали: Нет</b>")

@router.callback_query(F.data == "back")
async def callback_back(callback: CallbackQuery):
    """Нажатие кнопки Назад"""
    await callback.answer()
    await callback.message.edit_text(
        "📋 <b>Главное меню</b>",
        reply_markup=inline_menu()
    )

# ==================== ОБРАБОТКА МЕДИА ====================

@router.message(F.photo)
async def handle_photo(message: Message):
    """Получено фото"""
    await message.answer("📸 Красивое фото! Спасибо!")

@router.message(F.document)
async def handle_document(message: Message):
    """Получен документ"""
    file_name = message.document.file_name
    await message.answer(f"📄 Документ получен: <code>{file_name}</code>")

@router.message(F.sticker)
async def handle_sticker(message: Message):
    """Получен стикер"""
    await message.answer("👍 Классный стикер!")

# ==================== ЭХО (всё остальное) ====================

@router.message(F.text)
async def echo(message: Message):
    """Эхо для всех остальных сообщений"""
    await message.answer(
        f"💬 Вы написали: <i>{message.text}</i>\n\n"
        f"Используйте /help для списка команд."
    )

# ==================== FASTAPI ПРИЛОЖЕНИЕ ====================

app = FastAPI(title="Telegram Bot on BotHost", version="1.0.0")

@app.on_event("startup")
async def on_startup():
    """Запуск бота"""
    logger.info("=" * 60)
    logger.info("🚀 ЗАПУСК БОТА")
    logger.info("=" * 60)
    logger.info(f"🔧 BOT_TOKEN: {'✅ Есть' if BOT_TOKEN else '❌ НЕТ'}")
    logger.info(f"🔧 WEBHOOK_HOST: {WEBHOOK_HOST if WEBHOOK_HOST else '❌ НЕТ'}")
    logger.info(f"🔧 WEBHOOK_URL: {WEBHOOK_URL}")
    logger.info(f"🔧 PORT: {PORT}")
    logger.info("=" * 60)
    
    # Регистрируем обработчики
    dp.include_router(router)
    
    # Удаляем старый webhook
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🗑️ Старый webhook удалён")
    except Exception as e:
        logger.error(f"❌ Ошибка удаления webhook: {e}")
        return
    
    # Устанавливаем новый webhook
    if WEBHOOK_URL and WEBHOOK_HOST and BOT_TOKEN:
        try:
            await bot.set_webhook(
                url=WEBHOOK_URL,
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"]
            )
            
            # Проверяем установку
            info = await bot.get_webhook_info()
            logger.info("✅ Webhook установлен!")
            logger.info(f"📡 URL: {info.url}")
            logger.info(f"📊 Pending: {info.pending_update_count}")
            
            if info.last_error_message:
                logger.warning(f"⚠️ Ошибка: {info.last_error_message}")
            
            logger.info("=" * 60)
            logger.info("✅ БОТ РАБОТАЕТ!")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Ошибка webhook: {e}")
    else:
        logger.error("❌ Переменные окружения не установлены!")

@app.on_event("shutdown")
async def on_shutdown():
    """Остановка бота"""
    logger.info("🛑 Остановка бота...")
    try:
        await bot.delete_webhook()
        await bot.session.close()
        logger.info("✅ Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка остановки: {e}")

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Главная страница"""
    return {
        "status": "ok",
        "bot": "running",
        "webhook": WEBHOOK_URL,
        "message": "Bot is working!",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check для BotHost"""
    return {"status": "ok", "healthy": True}

@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    """Обработка webhook от Telegram"""
    try:
        data = await request.json()
        update_id = data.get('update_id', 'unknown')
        logger.info(f"📨 Update #{update_id}")
        
        update = Update(**data)
        await dp.feed_update(bot=bot, update=update)
        
        return JSONResponse(content={"ok": True})
    except Exception as e:
        logger.error(f"❌ Ошибка webhook: {e}")
        return JSONResponse(content={"ok": True})

# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    logger.info(f"🚀 Запуск на порту {PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
```

4. **Прокрутите вниз и нажмите:** **"Commit new file"** (зелёная кнопка)

### 3.2 Создаём файл requirements.txt

1. **Снова нажмите:** **"Add file"** → **"Create new file"**

2. **В поле имени напишите:**
   ```
   requirements.txt
   ```

3. **В поле кода вставьте:**
   ```txt
   aiogram==3.4.1
   fastapi==0.109.0
   uvicorn[standard]==0.27.0
   ```

4. **Нажмите:** **"Commit new file"**

### 3.3 Создаём файл .env.example

1. **Снова нажмите:** **"Add file"** → **"Create new file"**

2. **В поле имени напишите:**
   ```
   .env.example
   ```

3. **В поле кода вставьте:**
   ```env
   # Токен бота от @BotFather
   BOT_TOKEN=your_token_here

   # URL хоста (получите в BotHost)
   WEBHOOK_HOST=https://your-bot.bothost.ru

   # Порт (обычно 3000)
   PORT=3000
   ```

4. **Нажмите:** **"Commit new file"**

### 3.4 Редактируем README.md

1. **Найдите файл README.md** в списке файлов

2. **Нажмите на него**, затем нажмите **значок карандаша** (Edit) справа

3. **Замените содержимое на:**
   ```markdown
   # 🤖 Мой Telegram бот на BotHost

   Простой Telegram бот, работающий на webhook через BotHost.

   ## Возможности
   - ✅ Команды (/start, /help, /menu)
   - ✅ Кнопки меню
   - ✅ Inline кнопки
   - ✅ Обратная связь
   - ✅ Обработка медиа

   ## Технологии
   - Python 3.11
   - aiogram 3.4
   - FastAPI
   - BotHost

   ## Автор
   Ваше имя
   ```

4. **Нажмите:** **"Commit changes"**

---

## 🌐 Шаг 4: Регистрация на BotHost

### 4.1 Переходим на сайт

1. **Откройте браузер**

2. **Перейдите на:** [https://bothost.ru](https://bothost.ru)

3. **Нажмите:** **"Войти"** или **"Регистрация"** (справа вверху)

### 4.2 Регистрация

4. **Если нет аккаунта:**
   - Нажмите **"Зарегистрироваться"**
   - Введите **Email**
   - Придумайте **Пароль**
   - Нажмите **"Зарегистрироваться"**

5. **Подтвердите email:**
   - Откройте почту
   - Найдите письмо от BotHost
   - Нажмите на ссылку подтверждения

6. **Войдите в аккаунт** с вашим email и паролем

### 4.3 Выбор тарифа

7. **Выберите тариф:**
   - Есть бесплатный тариф для начала
   - Нажмите **"Выбрать"** на нужном тарифе
   - Для тестирования подойдёт **"Базовый"** или **"Free"**

---

## 🔌 Шаг 5: Подключение к BotHost

### 5.1 Создание бота в панели

1. **В личном кабинете нажмите:** **"Создать бота"** или **"Добавить бота"**

2. **Заполните форму:**

   **Название бота:**
   ```
   My Awesome Bot
   ```
   
   **Платформа:**
   - Выберите **Telegram**
   
   **Язык программирования:**
   - Выберите **Python**
   
   **Git репозиторий:**
   - Вставьте URL вашего GitHub репозитория
   - Например: `https://github.com/your_username/my-telegram-bot`
   - **ОТКУДА ВЗЯТЬ:** это адрес который вы сохранили в Шаге 2.3

3. **Нажмите:** **"Создать"** или **"Далее"**

### 5.2 Настройка параметров

4. **Команда запуска:**
   - Обычно определяется автоматически
   - Если спрашивает, введите:
     ```
     python bot.py
     ```

5. **Ветка (Branch):**
   - Оставьте **main** или **master**

6. **Автообновление:**
   - Можно включить (бот будет обновляться при push в GitHub)
   - Скопируйте webhook URL если показывает

7. **Нажмите:** **"Сохранить"** или **"Создать бота"**

### 5.3 Получаем URL бота

8. **После создания вы увидите:**
   - Название бота
   - Статус (может быть "Остановлен" или "Ошибка" - это нормально)
   - **URL бота** (например: `https://mybot123.bothost.ru`)

9. **ВАЖНО: Скопируйте этот URL!**
   - Выделите мышкой
   - Ctrl+C (Cmd+C на Mac)
   - Сохраните в блокнот

---

## ⚙️ Шаг 6: Настройка переменных окружения

### 6.1 Открываем настройки переменных

1. **В панели BotHost:**
   - Найдите вашего бота в списке
   - Нажмите на него

2. **Найдите раздел:**
   - **"Переменные окружения"**
   - Или **"Environment Variables"**
   - Или **"Настройки"** → **"Переменные"**
   - Или значок **⚙️**

3. **Нажмите:** **"Добавить переменную"** или **"+"**

### 6.2 Добавляем BOT_TOKEN

4. **Первая переменная:**
   
   **Название (Name/Key):**
   ```
   BOT_TOKEN
   ```
   - Пишите ТОЧНО так, с большими буквами
   
   **Значение (Value):**
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567
   ```
   - **ОТКУДА ВЗЯТЬ:** Это токен который вы получили от BotFather в Шаге 1.3
   - Откройте блокнот где сохранили токен
   - Скопируйте ВЕСЬ токен
   - Вставьте сюда

5. **Нажмите:** **"Добавить"** или **"Сохранить"**

### 6.3 Добавляем WEBHOOK_HOST

6. **Вторая переменная:**

   **Нажмите:** **"Добавить переменную"** или **"+"**
   
   **Название (Name/Key):**
   ```
   WEBHOOK_HOST
   ```
   
   **Значение (Value):**
   ```
   https://mybot123.bothost.ru
   ```
   - **ОТКУДА ВЗЯТЬ:** Это URL который вы скопировали в Шаге 5.3
   - Откройте блокнот где сохранили URL
   - Скопируйте URL
   - ⚠️ ВАЖНО: URL должен начинаться с `https://`
   - ⚠️ ВАЖНО: БЕЗ слеша `/` в конце!

7. **Нажмите:** **"Добавить"** или **"Сохранить"**

### 6.4 Добавляем PORT (опционально)

8. **Третья переменная (если требуется):**

   **Название (Name/Key):**
   ```
   PORT
   ```
   
   **Значение (Value):**
   ```
   3000
   ```
   - Обычно BotHost сам определяет порт
   - Добавляйте только если в логах есть ошибка про порт

9. **Нажмите:** **"Добавить"** или **"Сохранить"**

### 6.5 Проверка переменных

10. **У вас должно быть минимум 2 переменные:**

| Название | Значение (пример) |
|----------|-------------------|
| `BOT_TOKEN` | `1234567890:ABCdef...` |
| `WEBHOOK_HOST` | `https://mybot123.bothost.ru` |

---

## 🚀 Шаг 7: Запуск и проверка

### 7.1 Запускаем бота

1. **В панели BotHost:**
   - Найдите кнопку **"Запустить"** или **"Start"**
   - Нажмите её

2. **Дождитесь запуска:**
   - Статус должен измениться на **"Работает"** или **"Running"**
   - Это может занять 10-30 секунд

### 7.2 Проверяем логи

3. **Откройте логи:**
   - Нажмите **"Логи"** или **"Logs"**
   - Или нажмите на бота → вкладка **"Логи работы"**

4. **Что должно быть в логах:**
   ```
   🚀 ЗАПУСК БОТА
   🔧 BOT_TOKEN: ✅ Есть
   🔧 WEBHOOK_HOST: https://mybot123.bothost.ru
   🔧 WEBHOOK_URL: https://mybot123.bothost.ru/webhook
   🗑️ Старый webhook удалён
   ✅ Webhook установлен!
   📡 URL: https://mybot123.bothost.ru/webhook
   ✅ БОТ РАБОТАЕТ!
   ```

5. **Если видите ошибки:**
   - Смотрите раздел [Решение проблем](#решение-проблем) ниже

### 7.3 Проверяем API

6. **Откройте в браузере:**
   ```
   https://ваш-бот.bothost.ru/
   ```
   - Замените `ваш-бот` на ваш реальный URL
   - **ОТКУДА ВЗЯТЬ:** URL из Шага 5.3

7. **Должны увидеть:**
   ```json
   {
     "status": "ok",
     "bot": "running",
     "webhook": "https://ваш-бот.bothost.ru/webhook",
     "message": "Bot is working!",
     "version": "1.0.0"
   }
   ```

### 7.4 Тестируем бота в Telegram

8. **Откройте Telegram**

9. **Найдите вашего бота:**
   - В поиске введите username бота
   - Например: `@my_awesome_bot`
   - **ОТКУДА ВЗЯТЬ:** username который вы создали в Шаге 1.2 (пункт 7)

10. **Нажмите START**

11. **Бот должен ответить:**
    ```
    👋 Привет, Ваше_Имя!

    🎉 Я работаю на BotHost!
    Используй меню ниже для навигации.
    ```
    - И показать кнопки меню

### 7.5 Проверяем функции

12. **Попробуйте команды:**
    - `/help` - должен показать список команд
    - `/menu` - должен показать inline меню
    - `/feedback` - должен запросить отзыв

13. **Попробуйте кнопки:**
    - Нажмите **"📋 Меню"** - должны появиться inline кнопки
    - Нажмите **"ℹ️ Информация"** - должна показаться информация о боте
    - Нажмите **"✅ Да"** в inline меню - должен ответить

14. **Попробуйте отправить:**
    - Текст - бот отправит эхо
    - Фото - бот ответит "📸 Красивое фото!"
    - Файл - бот покажет имя файла

15. **Проверьте логи в BotHost:**
    - Должны появиться записи типа:
      ```
      📨 Update #123456789
      ```

### 7.6 Если всё работает

16. **🎉 Поздравляю! Ваш бот работает!**

---

## 🔧 Решение проблем

### ❌ Проблема 1: "Unauthorized" в логах

**Что видите:**
```
TelegramUnauthorizedError: Telegram server says - Unauthorized
```

**Причина:**
- Неверный токен бота

**Решение:**

1. **Получите новый токен:**
   - Откройте Telegram → @BotFather
   - Отправьте `/mybots`
   - Выберите вашего бота
   - Нажмите **"API Token"**
   - Нажмите **"Revoke current token"** (отозвать текущий)
   - Подтвердите
   - **Скопируйте новый токен**

2. **Обновите в BotHost:**
   - Откройте переменные окружения
   - Найдите `BOT_TOKEN`
   - Замените на новый токен
   - Сохраните
   - Перезапустите бота

---

### ❌ Проблема 2: "Port already in use"

**Что видите:**
```
OSError: [Errno 98] address already in use
```

**Причина:**
- Порт занят или конфликт

**Решение:**

1. **В переменных окружения:**
   - Удалите переменную `PORT`
   - Или измените на `3000`
   - Сохраните
   - Перезапустите бота

---

### ❌ Проблема 3: Бот не отвечает

**Что видите:**
- Бот в статусе "Работает"
- Логи показывают "БОТ РАБОТАЕТ"
- Но в Telegram не отвечает

**Решение:**

1. **Проверьте webhook:**
   - В логах найдите строку с URL webhook
   - Скопируйте этот URL
   - Откройте в браузере
   - Должен быть ответ (даже если ошибка - значит работает)

2. **Проверьте переменные:**
   - `BOT_TOKEN` - должен быть правильный
   - `WEBHOOK_HOST` - должен быть `https://ваш-бот.bothost.ru`
   - БЕЗ `/webhook` в конце
   - БЕЗ слеша `/` в конце

3. **Сделайте hard reset:**
   - Остановите бота в BotHost
   - Подождите 10 секунд
   - Запустите снова

4. **Проверьте в @BotFather:**
   - Отправьте `/mybots`
   - Выберите бота
   - Убедитесь что он активен

---

### ❌ Проблема 4: "WEBHOOK_HOST не установлен"

**Что видите:**
```
❌ WEBHOOK_HOST не установлен!
```

**Причина:**
- Переменная окружения не создана или пустая

**Решение:**

1. **В BotHost:**
   - Откройте переменные окружения
   - Проверьте что есть `WEBHOOK_HOST`
   - Значение должно быть `https://ваш-бот.bothost.ru`
   - Без лишних пробелов

2. **Откуда взять URL:**
   - В панели BotHost
   - Рядом с названием бота
   - Или в разделе "Информация"
   - Копируйте ВЕСЬ URL с `https://`

---

### ❌ Проблема 5: "Module not found"

**Что видите:**
```
ModuleNotFoundError: No module named 'aiogram'
```

**Причина:**
- Не установлены зависимости

**Решение:**

1. **Проверьте файл requirements.txt:**
   - Зайдите в GitHub репозиторий
   - Откройте `requirements.txt`
   - Должно быть:
     ```
     aiogram==3.4.1
     fastapi==0.109.0
     uvicorn[standard]==0.27.0
     ```

2. **Если файла нет:**
   - Создайте его (см. Шаг 3.2)

3. **Перезапустите бота в BotHost**

---

### ❌ Проблема 6: "404 Not Found" при открытии URL

**Что видите:**
- При открытии `https://ваш-бот.bothost.ru/` показывает 404

**Причина:**
- Бот не запущен
- Или FastAPI приложение не стартовало

**Решение:**

1. **Проверьте статус бота:**
   - Должен быть "Работает"

2. **Проверьте логи:**
   - Должна быть строка "✅ БОТ РАБОТАЕТ!"

3. **Если в логах ошибки:**
   - Решите их сначала
   - Потом перезапустите

---

### 💡 Общие советы

**Если ничего не помогает:**

1. **Проверьте все переменные:**
   ```
   BOT_TOKEN - есть токен от BotFather
   WEBHOOK_HOST - https://ваш-бот.bothost.ru
   ```

2. **Проверьте файлы в GitHub:**
   - `bot.py` - есть и содержит код
   - `requirements.txt` - есть и содержит зависимости

3. **Перезапустите бота:**
   - Остановите
   - Подождите 10 секунд
   - Запустите

4. **Пересоздайте бота в BotHost:**
   - Удалите текущего
   - Создайте заново
   - Укажите те же настройки

5. **Обратитесь в поддержку BotHost:**
   - Email: support@bothost.ru
   - Опишите проблему
   - Приложите скриншоты логов

---

## 📊 Чек-лист успешного запуска

Перед запуском проверьте:

- [ ] Создан бот в @BotFather
- [ ] Получен и сохранён токен
- [ ] Создан GitHub репозиторий
- [ ] Файл `bot.py` загружен
- [ ] Файл `requirements.txt` загружен
- [ ] Зарегистрирован на BotHost
- [ ] Создан бот в BotHost
- [ ] Подключен GitHub репозиторий
- [ ] Добавлена переменная `BOT_TOKEN`
- [ ] Добавлена переменная `WEBHOOK_HOST`
- [ ] `WEBHOOK_HOST` начинается с `https://`
- [ ] `WEBHOOK_HOST` БЕЗ слеша в конце
- [ ] Бот запущен
- [ ] В логах есть "✅ БОТ РАБОТАЕТ!"
- [ ] URL открывается и показывает JSON
- [ ] Бот отвечает на /start

---

## 🎓 Что дальше?

После успешного запуска вы можете:

### 1. Добавить новые команды

В файле `bot.py` добавьте:
```python
@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer("📖 О боте\n\nЭто мой первый бот!")
```

### 2. Добавить базу данных

- SQLite для простых задач
- PostgreSQL для больших проектов

### 3. Добавить администраторские функции

- Проверка ID пользователя
- Рассылка сообщений
- Статистика

### 4. Добавить платежи

- Telegram Payments
- ЮKassa
- Stripe

### 5. Добавить MiniApp

- Создайте веб-интерфейс
- Интегрируйте с ботом

### 6. Добавить AI

- OpenAI GPT
- Другие AI сервисы

---

## 📚 Полезные ссылки

- [Документация aiogram](https://docs.aiogram.dev/en/latest/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotHost.ru](https://bothost.ru)
- [GitHub Docs](https://docs.github.com)
- [Python Tutorial](https://docs.python.org/3/tutorial/)

---

## 🆘 Нужна помощь?

**Telegram каналы:**
- BotHost - группа поддержки (ссылка на сайте)

**Email:**
- BotHost: support@bothost.ru

**Документация:**
- BotHost: на сайте в разделе "Документация"

---

## ✅ Заключение

🎉 **Поздравляю!** Вы создали своего первого Telegram бота на webhook и развернули его на BotHost!

Теперь вы знаете:
- ✅ Как создать бота через @BotFather
- ✅ Как работать с GitHub
- ✅ Как использовать BotHost
- ✅ Как настраивать переменные окружения
- ✅ Как проверять и отлаживать бота

**Удачи в разработке! 🚀**

---

*Мануал создан: 28.01.2026*  
*Версия: 1.0*
