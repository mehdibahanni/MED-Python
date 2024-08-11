import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import API_TOKEN, CHAT_ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def fetch_options_data():
    url = 'WEBULL_API_ENDPOINT'  # استبدل بالعنوان المناسب
    params = {
        # المعلمات المناسبة للطلب
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data

async def analyze_and_notify():
    data = await fetch_options_data()
    for option in data['options']:
        volume = option['volume']
        if volume > 500:
            message = (f"اسم السهم: ${option['symbol']}\n"
                       f"تاريخ انتهاء العقد: {option['expiration_date']}\n"
                       f"الاسترايك: {option['strike_price']}\n"
                       f"نوع الصفقة: {option['trade_type']}\n"
                       f"سعر الصفقة: {option['trade_price']}\n"
                       f"حجم الصفقة: {option['volume']}\n\n"
                       f"سعر ASK: {option['ask_price']}\n"
                       f"سعر BID: {option['bid_price']}\n\n"
                       f"حجم التداول: {option['total_volume']}\n"
                       f"عدد صفقات اليوم: {option['trades_today']}\n"
                       f"سعر الافتتاح: {option['opening_price']}\n"
                       f"أعلى سعر: {option['highest_price']}\n"
                       f"أدنى سعر: {option['lowest_price']}\n"
                       f"سعر الإغلاق: {option['closing_price']}\n"
                       f"مشتري BID")
            await bot.send_message(CHAT_ID, message, parse_mode=ParseMode.MARKDOWN)

async def periodic_check():
    while True:
        await analyze_and_notify()
        await asyncio.sleep(60)  # الانتظار لمدة 60 ثانية قبل التحقق مرة أخرى

async def on_startup(dispatcher):
    asyncio.create_task(periodic_check())

if __name__ == '_main_':
    executor.start_polling(dp, on_startup=on_startup)
