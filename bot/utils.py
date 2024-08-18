from telegram import  InlineKeyboardButton,InlineKeyboardMarkup, Update
import os
import asyncio
from telegram.ext import  ContextTypes, ConversationHandler
ASK_NAME,ASK_AGE,ASK_CITY, PROCESS_CITY,SAVING_PHOTO,SAVING_VIDEO,PROCESS_DELETE_CONFIRMATION1,PROCESS_DELETE_CONFIRMATION2,PROCESS_MENU=range(9)

menu_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Узнать текущую погоду", callback_data='weather')],
                [InlineKeyboardButton("Сбросить настройки", callback_data='default')],
                [InlineKeyboardButton('Выгрузить видео', callback_data='send_video')],
                [InlineKeyboardButton('Выгрузить фото', callback_data='send_photo')],
                [InlineKeyboardButton('Сохранить видео', callback_data='save_video')],
                [InlineKeyboardButton('Сохранить фото', callback_data='save_photo')],
            ])

def delete_all_files_in_directory(directory_path):
    if os.path.exists(directory_path):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif','.mp4')):
                os.remove(file_path)
    else:
        print(f"Папка {directory_path} не найдена.")

async def askingInfo(update:Update, context:ContextTypes.DEFAULT_TYPE, message)->None:
    if update.callback_query:
         await update.callback_query.edit_message_text(message)
    elif update.message:
         await update.message.reply_text(message)
async def isUserExist(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    if update.callback_query:
         user= update.callback_query.from_user
    elif update.message:
         user= update.message.from_user
     
    username=user.username
    userId=user.id 
    return(username,userId)   