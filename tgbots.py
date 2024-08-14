
from telegram import Update
import requests
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import os
from datetime import datetime
ASK_NAME,ASK_COLOR,ASK_CITY, WAITING_FOR_COMMAND=range(4)
async def start (update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    name=context.user_data.get('name',None)
    color=context.user_data.get('color',None)
    city=context.user_data.get('city',None)
    if bool(color) and bool(name) :
        await update.message.reply_text(f'Привет {name}, я помню, твой любимый цвет - {color} и ты живешь в {city}')
        return WAITING_FOR_COMMAND
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
    return ASK_CITY
async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['city'] = update.message.text
    await update.message.reply_text("Используя комманду /weather , вы сможете узнать погоду")
    return WAITING_FOR_COMMAND
async def default(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    context.user_data.clear()
    await update.message.reply_text('Данные очищены')
    return await start(update, context)
async def waiting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Я жду ваших команд. Вы можете использовать /default для сброса данных.")
    return WAITING_FOR_COMMAND
async def cancel(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    await update.message.reply_text('Диалог завершен')
    return ConversationHandler.END  
async def send_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join("video")
    if len(os.listdir(directory))==0:
        await update.message.reply_text("Не найдено фото для отправки")
    # Проходим по всем файлам в директории
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Проверяем, что файл является изображением (по расширению)
        if file_name.lower().endswith((".mp4")):
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video)
    
    await update.message.reply_text("Все видео отправлены.")  
    return WAITING_FOR_COMMAND
async def send_photo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join("photo")
    if len(os.listdir(directory))==0:
        await update.message.reply_text("Не найдено фото для отправки")
    # Проходим по всем файлам в директории
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Проверяем, что файл является изображением (по расширению)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            with open(file_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
    
    await update.message.reply_text("Все фото отправлены.")
    return WAITING_FOR_COMMAND
async def save_photo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    # Путь к директории
    directory = os.path.join( "photo")
  
    # Получаем текущую временную метку
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Формируем имя файла с временной меткой
    file_name = f"{context.user_data['name']}_{timestamp}.jpg"
    photo_path = os.path.join(directory, file_name)

    # Скачиваем файл и сохраняем его
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(custom_path=photo_path)

    await update.message.reply_text(f"Фото успешно сохранено. Используя команду /send_photo вы можете вызвать все сохраненные фото")
    return WAITING_FOR_COMMAND
async def save_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    # Путь к директории
    directory = os.path.join("video")
  
    # Получаем текущую временную метку
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Формируем имя файла с временной меткой
    file_name = f"{context.user_data['name']}_{timestamp}.mp4"
    video_path = os.path.join(directory, file_name)

    # Скачиваем файл и сохраняем его
    video_file = await update.message.video.get_file()
    await video_file.download_to_drive(custom_path=video_path)

    await update.message.reply_text(f"Видео успешно сохранено. Используя команду /send_video вы можете вызвать все сохраненные видео")
    return WAITING_FOR_COMMAND
async def weather(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
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
        await update.message.reply_text(f"Погода в {city}: {weather}\nТемпература: {temp}°C")  
        return WAITING_FOR_COMMAND 
cnv_handler=ConversationHandler(
    entry_points=[CommandHandler('start',start)],
    states={
        ASK_NAME:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_name)],
        ASK_COLOR:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_color)],
        ASK_CITY:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_city)],
        WAITING_FOR_COMMAND: [
            MessageHandler(filters.PHOTO, save_photo), 
            MessageHandler(filters.VIDEO, save_video), 
            CommandHandler("weather", weather),
            CommandHandler("send_photo", send_photo),
            CommandHandler("send_video", send_video),
            CommandHandler("video", send_video),
            MessageHandler(filters.TEXT and ~filters.COMMAND, waiting)
        ],
    },
    fallbacks=[CommandHandler('cancel',cancel),CommandHandler('default',default)])
app = ApplicationBuilder().token("6867300294:AAEXa-svt9_x3Yt7q66tOAcCwYkPmBNLQwY").build()
app.add_handler(cnv_handler)

app.run_polling()
