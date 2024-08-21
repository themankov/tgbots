from telegram import  InlineKeyboardButton,InlineKeyboardMarkup, Update
import os
import asyncio
from telegram.ext import  ContextTypes, ConversationHandler
ASK_NAME,ASK_AGE,ASK_CITY, PROCESS_CITY,SAVING_PHOTO,SAVING_VIDEO,PROCESS_DELETE_CONFIRMATION1,PROCESS_DELETE_CONFIRMATION2,PROCESS_MENU, SETTING_PLANS,MARK_PLAN, ADD_WATERMARK, PROCESS_PHOTO=range(13)

menu_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Узнать текущую погоду", callback_data='weather')],
                [InlineKeyboardButton("Сбросить настройки", callback_data='default')],
                [InlineKeyboardButton('Работа с видео', callback_data='video')],
                [InlineKeyboardButton('Работа с фото', callback_data='photo')],
                [InlineKeyboardButton('Работа с постами', callback_data='plans')],
            ])
video_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Сохранить видео", callback_data='save_video')],
                [InlineKeyboardButton("Добавить водяной знак", callback_data='add_photo_watermark')],
                [InlineKeyboardButton("Выгрузить видео", callback_data='send_video')],
            ])
photo_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Загрузить фото", callback_data='save_photo')],
                [InlineKeyboardButton("Выгрузить фото", callback_data='send_photo')],
            ])
photo_edit_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Повернуть фото", callback_data='rotate_photo')],
                [InlineKeyboardButton("Назад", callback_data='go_back')],

            ])
rotate_photo_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Повернуть по часовой стрелке", callback_data='rotate_photo_right')],
                [InlineKeyboardButton("Повернуть против часовой стрелки", callback_data='rotate_photo_left')],

            ])
plans_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Сформировать новую цель", callback_data='set_plans')],
                [InlineKeyboardButton("Показать список целей", callback_data='get_plans')],
                [InlineKeyboardButton("Показать завершенные цели", callback_data='get_finished_plans')],
            ])
def delete_all_files_in_directory(directory_path):
    if os.path.exists(directory_path):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif','.mp4')):
                os.remove(file_path)
    else:
        print(f"Папка {directory_path} не найдена.")

async def askingInfoEdit(update:Update, context:ContextTypes.DEFAULT_TYPE, message)->None:
    if update.callback_query:
         await update.callback_query.edit_message_text(message)
    elif update.message:
         await update.message.edit_text(message)
async def askingInfoMessage(update:Update, context:ContextTypes.DEFAULT_TYPE, message)->None:
      if update.callback_query:
                    await update.callback_query.message.reply_text(message)
      else:
                    await update.message.reply_text(message) 

async def isUserExist(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    if update.callback_query:
         user= update.callback_query.from_user
    elif update.message:
         user= update.message.from_user
     
    username=user.username
    userId=user.id 
    return(username,userId)   