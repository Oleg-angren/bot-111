import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os

# Логирование
logging.basicConfig(level=logging.INFO)

# Загружаем переменные
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в переменных окружения")

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Бот запущен! Работает 24/7 на Render.com")

# Обработчик /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Я просто эхо-бот. Пиши что угодно!")

# Эхо-обработчик
@dp.message()
async def echo(message: types.Message):
    try:
        await message.answer(f"Вы сказали:\n> {message.text}")
    except Exception as e:
        logging.error(f"Ошибка при ответе: {e}")

# Запуск бота
async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
