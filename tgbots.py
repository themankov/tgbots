
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton,InlineKeyboardMarkup
import requests
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler,CallbackQueryHandler
import os
import asyncio
from datetime import datetime
ASK_NAME,ASK_COLOR,ASK_CITY, PROCESS_CITY,SAVING_PHOTO,SAVING_VIDEO,PROCESS_DELETE_CONFIRMATION1,PROCESS_DELETE_CONFIRMATION2,PROCESS_MENU=range(9)
async def start (update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    name=context.user_data.get('name',None)
    color=context.user_data.get('color',None)
    city=context.user_data.get('city',None)
    if bool(color) and bool(name) and bool(city):
        await update.message.reply_text(f'Привет {name}, я помню, твой любимый цвет - {color} и ты живешь в {city}')
        return await menu(update, context)
    elif update.callback_query:
            await update.callback_query.message.reply_text("Как тебя зовут?")  
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
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    context.user_data['city'] = query.data
    return await menu(update,context)   
async def default(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    keyboard=[
        [InlineKeyboardButton('Удалить все данные', callback_data='delete_data')] 
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
            await update.callback_query.message.reply_text("Выберите действие",reply_markup=markup)
    else:
            await update.message.reply_text("Выберите действие",reply_markup=markup)
    return PROCESS_DELETE_CONFIRMATION1
async def confirm_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Да", callback_data='delete')],
        [InlineKeyboardButton("Нет", callback_data='cancel')],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Вы уверены, что хотите удалить все данные?", reply_markup=markup)
    return PROCESS_DELETE_CONFIRMATION2
async def delete_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data=='delete':
        #TODO: Удаление из папок
        context.user_data.clear()
        await query.edit_message_text("Все данные успешно удалены.")
    elif query.data=='cancel':   
         await query.edit_message_text("Удаление отменено.")
         return await menu(update,context)
    return await start(update,context)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Удаление отменено")
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Узнать текущую погоду", callback_data='weather')],
        [InlineKeyboardButton("Сбросить настройки", callback_data='default')],
        [InlineKeyboardButton('Выгрузить видео', callback_data='send_video')],
        [InlineKeyboardButton('Выгрузить фото', callback_data='send_photo')],
        [InlineKeyboardButton('Сохранить видео', callback_data='save_video')],
        [InlineKeyboardButton('Сохранить фото', callback_data='save_photo')],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    try:
        # Если это callback_query
        if update.callback_query:
            await update.callback_query.edit_message_text("Выберите действие", reply_markup=markup)
        # Если это обычное сообщение
        elif update.message:
            await update.message.reply_text("Выберите действие", reply_markup=markup)
        else:
            print("Непредвиденный тип объекта update")
            return PROCESS_MENU
    except AttributeError as e:
        print(f"Ошибка при попытке открыть меню: {e}")
        if hasattr(update, 'message') and update.message:
            await update.message.reply_text("Произошла ошибка при открытии меню.")
    return PROCESS_MENU
async def menu_choice(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    query=update.callback_query
    await query.answer()

    if query.data=='weather':
        return await weather(update, context)
    elif query.data =='default':
        return await default(update,context)
    elif query.data == 'send_video':
        return await send_video(update,context)
    elif query.data =='send_photo':
        print(update)
        return await send_photo(update,context)
    elif query.data =='save_photo':
        await query.edit_message_text("Пришлите фото, которое планируете сохранить")
        return SAVING_PHOTO
    elif query.data =='save_video':
        await query.edit_message_text("Пришлите видео, которое планируете сохранить")
        return SAVING_VIDEO
async def cancel(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    await update.message.reply_text('Диалог завершен')
    return ConversationHandler.END  
async def send_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join("video")
    if len(os.listdir(directory))==0:
        await update.message.reply_text("Не найдено фото для отправки")
        return await menu(update,context)
    
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

       
        if file_name.lower().endswith((".mp4")):
            with open(file_path, 'rb') as video:
                if update.callback_query:
                    await update.callback_query.message.reply_video(video=video)
                else:
                     await update.message.reply_video(video=video) 
    
    if update.callback_query:
            await update.callback_query.message.reply_text("Все видео отправлены")  
    else:
            await update.message.reply_text("Все видео отправлены")
    await update.callback_query.message.reply_text(
            text="Выберите действие:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Узнать текущую погоду", callback_data='weather')],
                [InlineKeyboardButton("Сбросить настройки", callback_data='default')],
                [InlineKeyboardButton('Выгрузить видео', callback_data='send_video')],
                [InlineKeyboardButton('Выгрузить фото', callback_data='send_photo')],
                [InlineKeyboardButton('Сохранить видео', callback_data='save_video')],
                [InlineKeyboardButton('Сохранить фото', callback_data='save_photo')],
            ])
        )
async def send_photo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join("photo")
    if len(os.listdir(directory))==0:
        await update.message.reply_text("Не найдено фото для отправки")
        return await menu(update,context)
   
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            with open(file_path, 'rb') as photo:
                if update.callback_query:
                    await update.callback_query.message.reply_photo(photo=photo)
                else:
                     await update.message.reply_photo(photo=photo)   
    
    if update.callback_query:
            await update.callback_query.message.reply_text("Все фото отправлены")  
    else:
            await update.message.reply_text("Все фото отправлены")
    
    # Возвращаем меню
    await update.callback_query.message.reply_text(
            text="Выберите действие:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Узнать текущую погоду", callback_data='weather')],
                [InlineKeyboardButton("Сбросить настройки", callback_data='default')],
                [InlineKeyboardButton('Выгрузить видео', callback_data='send_video')],
                [InlineKeyboardButton('Выгрузить фото', callback_data='send_photo')],
                [InlineKeyboardButton('Сохранить видео', callback_data='save_video')],
                [InlineKeyboardButton('Сохранить фото', callback_data='save_photo')],
            ])
        )
async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    directory = os.path.join("photo")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{context.user_data['name']}_{timestamp}.jpg"
    photo_path = os.path.join(directory, file_name)

    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(custom_path=photo_path)

    try:
        if update.callback_query:
            await update.callback_query.message.reply_text("Фото сохранено")
            return await menu(update, context)
        else:
            await update.message.reply_text("Фото сохранено")
            return await menu(update, context)
    except AttributeError as e:
        print(f"Ошибка при вызове меню: {e}")
        if update.message:
            await update.message.reply_text("Произошла ошибка при открытии меню.")
async def save_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join("video")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{context.user_data['name']}_{timestamp}.mp4"
    video_path = os.path.join(directory, file_name)

    video_file = await update.message.video.get_file()
    await video_file.download_to_drive(custom_path=video_path)

    if update.callback_query:
        await update.callback_query.message.reply_text("Видео сохранено")
    else:
        await update.message.reply_text("Видео сохранено")
    return await menu(update,context)
async def weather(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    updateBuff=update
    city = context.user_data['city']
    if not city:
        await update.message.reply_text("Пожалуйста, укажите название города после команды /weather.")
        return ASK_CITY
    API_KEY="a287264f20a31a7533cb7c1785bd82f1"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
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
            await update.message.reply_text(f"Погода в {city}: {weather}\nТемпература: {temp}°C")
            
        
        # Задержка, чтобы пользователь увидел результат
        await asyncio.sleep(5)  # Задержка в 5 секунд

        # Возвращаем меню
        await update.callback_query.edit_message_text(
            text="Выберите действие:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Узнать текущую погоду", callback_data='weather')],
                [InlineKeyboardButton("Сбросить настройки", callback_data='default')],
                [InlineKeyboardButton('Выгрузить видео', callback_data='send_video')],
                [InlineKeyboardButton('Выгрузить фото', callback_data='send_photo')],
                [InlineKeyboardButton('Сохранить видео', callback_data='save_video')],
                [InlineKeyboardButton('Сохранить фото', callback_data='save_photo')],
            ])
        )

cnv_handler=ConversationHandler(
    entry_points=[CommandHandler('start',start)],
    states={
        ASK_NAME:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_name)],
        ASK_COLOR:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_color)],
        PROCESS_CITY:[CallbackQueryHandler(button)],
        PROCESS_DELETE_CONFIRMATION1:[CallbackQueryHandler(confirm_delete)],
        PROCESS_DELETE_CONFIRMATION2:[CallbackQueryHandler(delete_data)],
        PROCESS_MENU:[CallbackQueryHandler(menu_choice)],
        SAVING_PHOTO:[MessageHandler(filters.PHOTO,save_photo)],
        SAVING_VIDEO:[MessageHandler(filters.VIDEO,save_video)],
    },
    per_message=False,
    fallbacks=[CommandHandler('start',start)])
app = ApplicationBuilder().token("6867300294:AAEXa-svt9_x3Yt7q66tOAcCwYkPmBNLQwY").build()
app.add_handler(cnv_handler)

app.run_polling()
