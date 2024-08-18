from telegram import Update
import requests
from telegram.ext import  ContextTypes
import asyncio
from .config import API_KEY_WEATHER
from .utils import *
async def weather(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:

    city = context.user_data['city']
    if not city:
        await update.message.reply_text("Пожалуйста, укажите название города после команды /weather.")
        return ASK_CITY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != 200:
        await update.message.reply_text(f"Город {city} не найден. Попробуйте еще раз написать город.")
        return ASK_CITY
    else:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]

        if update.callback_query:
            await update.callback_query.edit_message_text(f"Погода в {city}: {weather}\nТемпература: {temp}°C") 
            
        else:
            await update.message.edit_text(f"Погода в {city}: {weather}\nТемпература: {temp}°C")
            
        # Задержка, чтобы пользователь увидел результат
        await asyncio.sleep(5)  

        # Возвращаем меню
        await update.callback_query.edit_message_text(
            text="Выберите действие:",
            reply_markup=menu_markup
        )
