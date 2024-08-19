from telegram import Update
from telegram.ext import  ContextTypes
import os
from datetime import datetime
from .utils import *
from .menu import menu

async def video(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    markup = video_markup

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

async def send_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'video')
    if len(os.listdir(directory))==0:
        await askingInfoEdit(update,context,'Не найдено фото для отправки') 
        return await menu(update,context)
    await askingInfoEdit(update,context,'Готовим видео к выгрузке') 
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

       
        if file_name.lower().endswith((".mp4")):
            with open(file_path, 'rb') as video:
                if update.callback_query:
                    await update.callback_query.message.reply_video(video=video)
                else:
                     await update.message.reply_video(video=video) 
    
    await askingInfoEdit(update,context,"Все фото отправлены")
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

    await askingInfoEdit(update,context,"Видео сохранено")
    return await menu(update,context)
