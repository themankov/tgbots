from telegram import Update
from telegram.ext import  ContextTypes
import os
import io
import asyncio
from PIL import Image
from .database import session
from datetime import datetime
from .utils import *
from .menu import menu


directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'photo')
async def photo(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    markup = photo_markup

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

async def send_photo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    if len(os.listdir(directory))==0:
        await askingInfoEdit(update, context, "Не найдено фото для отправки")
        return await menu(update,context)
    await askingInfoEdit(update, context, "Готовим фото для выгрузки")
    photo_bytes=await get_photo(update,context)
    if update.callback_query:
                    await update.callback_query.message.reply_photo(photo=photo_bytes)
    else:
                     await update.message.reply_photo(photo=photo)  
    
    await askingInfoEdit(update, context, "Все фото отправлены")
    await asyncio.sleep(3)
    
    # Возвращаем меню
    await update.callback_query.message.reply_text(
            text="Выберите действие:",
            reply_markup=menu_markup
        )
async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #удаляем старые сохраненные файлы
    delete_all_files_in_directory(directory)

    #формирууем название файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{context.user_data['name']}_{timestamp}.jpg"
   
   # Скачиваем фото
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()

     # Скачиваем содержимое файла как байты
    photo_bytes = await photo_file.download_as_bytearray()
    
    # Открываем изображение с помощью Pillow
    image = Image.open(io.BytesIO(photo_bytes))
    
# Сохраняем измененное изображение во временный файл
    temp_file_path = os.path.join(directory, file_name)
    image.save(temp_file_path)

    await askingInfoMessage(update, context, "Фото сохранено")
    return await edit_photo(update,context)
async def edit_photo(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:

    markup = photo_edit_markup

    try:
        # Если это callback_query
        if update.callback_query:
            await update.callback_query.edit_message_text("Выберите действие", reply_markup=markup)
        # Если это обычное сообщение
        elif update.message:
            await update.message.reply_text("Выберите действие", reply_markup=markup)
        else:
            print("Непредвиденный тип объекта update")
            return PROCESS_PHOTO
    except AttributeError as e:
        print(f"Ошибка при попытке открыть меню: {e}")
        if hasattr(update, 'message') and update.message:
            await update.message.reply_text("Произошла ошибка при открытии меню.")
    return PROCESS_PHOTO

async def rotate_photo(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:

    markup = rotate_photo_markup

    try:
        # Если это callback_query
        if update.callback_query:
            await update.callback_query.edit_message_text("Выберите действие", reply_markup=markup)
        # Если это обычное сообщение
        elif update.message:
            await update.message.reply_text("Выберите действие", reply_markup=markup)
        else:
            print("Непредвиденный тип объекта update")
            return PROCESS_PHOTO
    except AttributeError as e:
        print(f"Ошибка при попытке открыть меню: {e}")
        if hasattr(update, 'message') and update.message:
            await update.message.reply_text("Произошла ошибка при открытии меню.")
    return PROCESS_PHOTO

async def rotate_options_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    query=update.callback_query
    await query.answer()  
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{context.user_data['name']}_{timestamp}.jpg"
    photo_bytes = await get_photo(update, context)
    delete_all_files_in_directory(directory)

    image =Image.open(io.BytesIO(photo_bytes))
    rotate_image=None
    if (query.data.endswith('left')):
        rotate_image =  image.rotate(90)
    elif (query.data.endswith('right')):
        rotate_image=image.rotate(-90)

# Сохраняем измененное изображение во временный файл
    temp_file_path = os.path.join(directory, file_name)
    rotate_image.save(temp_file_path)

    await askingInfoEdit(update, context, "Изменения сохранены")
    return await edit_photo(update,context)

async def get_photo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    photo=None
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            with open(file_path, 'rb') as photo:
                photo=photo
                photo_bytes=photo.read()
    return photo_bytes

async def add_photo_watermark(update:Update, context:ContextTypes.DEFAULT_TYPE):
     pass