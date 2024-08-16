from telegram import Update
from telegram.ext import  ContextTypes
import os
from datetime import datetime
from .utils import *
from .menu import menu

async def send_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'video')
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
            reply_markup=menu_markup
        )

async def save_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'video')
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
