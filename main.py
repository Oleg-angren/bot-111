import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
import os

# === Логирование ===
logging.basicConfig(level=logging.INFO)

# === Загрузка токена ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан")

# === Бот aiogram ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Бот работает! 🚀")

@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# === Веб-сервер для keep-alive ===
app = Flask('')

@app.route('/')
def home():
    return "Бот работает в фоне!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# === Запуск бота и веб-сервера ===
async def main():
    # Запускаем Flask в отдельном потоке
    thread = Thread(target=run_flask, daemon=True)
    thread.start()

    # Запускаем бота
    logging.info("Запуск бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
