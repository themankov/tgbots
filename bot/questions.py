from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import  ContextTypes
from .utils import *
from .menu import menu

async def start (update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    name=context.user_data.get('name',None)
    color=context.user_data.get('color',None)
    city=context.user_data.get('city',None)
    if bool(color) and bool(name) and bool(city):
        await update.message.reply_text(f'Привет {name}, я помню, твой любимый цвет - {color} и ты живешь в {city}')
        return await menu(update, context)
    elif update.callback_query:
            await update.callback_query.edit_message_text("Как тебя зовут?")  
    else:
            await update.message.reply_text('Как тебя зовут?')
    return ASK_NAME 
    
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f"Приятно познакомиться, {context.user_data['name']}! Какой твой любимый цвет?")
    return ASK_COLOR
async def ask_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['color'] = update.message.text
    await update.message.reply_text(f"Отлично! Я запомню, что твой любимый цвет — {context.user_data['color']}. Напиши мне свой город, чтобы узнать погоду")
    return await ask_city(update,context)
async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Москва", callback_data='Москва')],
        [InlineKeyboardButton("Санкт-Петербург", callback_data='Санкт-Петербург')],
        [InlineKeyboardButton('Волгоград',callback_data='Волгоград')]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите город",reply_markup=markup)
    return PROCESS_CITY
async def processing_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    context.user_data['city'] = query.data
    return await menu(update,context)   
