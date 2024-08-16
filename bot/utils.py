from telegram import  InlineKeyboardButton,InlineKeyboardMarkup
import os
ASK_NAME,ASK_COLOR,ASK_CITY, PROCESS_CITY,SAVING_PHOTO,SAVING_VIDEO,PROCESS_DELETE_CONFIRMATION1,PROCESS_DELETE_CONFIRMATION2,PROCESS_MENU=range(9)

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