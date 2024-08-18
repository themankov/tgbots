from telegram import Update
from telegram.ext import  ContextTypes
import os
from datetime import datetime
from .utils import *
from .menu import menu


async def send_photo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'photo')
    if len(os.listdir(directory))==0:
        await askingInfo(update, context, "Не найдено фото для отправки")
        return await menu(update,context)
    await askingInfo(update, context, "Готовим фото для выгрузки")
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            with open(file_path, 'rb') as photo:
                if update.callback_query:
                    await update.callback_query.message.reply_photo(photo=photo)
                else:
                     await update.message.reply_photo(photo=photo)   
    
    await askingInfo(update, context, "Все фото отправлены")
    
    # Возвращаем меню
    await update.callback_query.message.reply_text(
            text="Выберите действие:",
            reply_markup=menu_markup
        )
async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'photo')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{context.user_data['name']}_{timestamp}.jpg"
    photo_path = os.path.join(directory, file_name)

    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(custom_path=photo_path)

    await askingInfo(update, context, "Фото сохранено")
    return await menu(update,context)
    