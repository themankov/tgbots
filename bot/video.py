from telegram import Update
from telegram.ext import  ContextTypes
import os
from datetime import datetime
from .utils import *
from .menu import menu
from moviepy.editor import VideoFileClip,TextClip,CompositeVideoClip
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe"})
directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'video')

async def video_edit_options(update:Update,context:ContextTypes.DEFAULT_TYPE,markup)->None:
    if update.callback_query:
            await update.callback_query.edit_message_text("Выберите действие", reply_markup=markup)
        # Если это обычное сообщение
    elif update.message:
            await update.message.reply_text("Выберите действие", reply_markup=markup)
    else:
            print("Непредвиденный тип объекта update")
    return PROCESS_VIDEO


def video_edit_decorator(func):
    async def wrapper(update:Update,context:ContextTypes.DEFAULT_TYPE):
        if len(os.listdir(directory))==0:
            await askingInfoMessage(update,context,'Не найдено видео для отправки') 
            return await video_edit_options(update,context,markup=video_markup)
        clip=await func(update,context)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{context.user_data['name']}_{timestamp}.mp4"
        video_path = os.path.join(directory, file_name)
        clip.write_videofile(video_path, codec="libx264")
        clip.close()
        await askingInfoMessage(update,context,'Применяем изменения...')
        return await video_edit_options(update,context,markup=video_markup)
    return wrapper

async def send_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    if len(os.listdir(directory))==0:
        await askingInfoEdit(update,context,'Не найдено видео для отправки') 
        return await menu(update,context)
    await askingInfoEdit(update,context,'Готовим видео к выгрузке') 
    clip= await get_video()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{context.user_data['name']}_{timestamp}.mp4"
    video_path = os.path.join(directory, file_name)
    
    clip.write_videofile(video_path, codec="libx264")
    clip.close()

    files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.mp4')]
    
    # Сортируем файлы по времени модификации
    files.sort(key=os.path.getmtime, reverse=True)

    # Берем последний файл (самый новый)
    latest_video_path = files[0]
    with open(latest_video_path, 'rb') as video:
        if update.callback_query:
            await update.callback_query.message.reply_video(video=video)
        else:
            await update.message.reply_video(video=video)
    delete_all_files_in_directory(directory) 
    
    await askingInfoEdit(update,context,"Все фото отправлены")
    await update.callback_query.message.reply_text(
            text="Выберите действие:",
            reply_markup=menu_markup
        )
    return PROCESS_MENU

async def save_video(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{context.user_data['name']}_{timestamp}.mp4"
    video_path = os.path.join(directory, file_name)

    video_file = await update.message.video.get_file()
    await video_file.download_to_drive(custom_path=video_path)

    await askingInfoMessage(update,context,"Видео сохранено")
    return await video_edit_options(update,context,markup=video_markup)

async def get_video():
        files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.mp4')]
    
    # Сортируем файлы по времени модификации
        files.sort(key=os.path.getmtime, reverse=True)

    # Берем последний файл (самый новый)
        latest_video_path = files[0]

        video= VideoFileClip(latest_video_path )
      
        return video
@video_edit_decorator
async def cut(update:Update,context:ContextTypes.DEFAULT_TYPE):
    start=context.user_data['start']
    end=context.user_data['end']
    clip=await get_video()
   
    return clip.subclip(start,end)

@video_edit_decorator
async def slow_video(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
     clip= await get_video()
     return clip.speedx(factor=0.5)
@video_edit_decorator
async def fast_video(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
     clip= await get_video()
     return clip.speedx(factor=2)

@video_edit_decorator
async def add_watermark(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    clip= await get_video()

    watermark_text=update.message.text

    # Создание текстового клипа
    text_clip = TextClip(watermark_text, fontsize=70, color='white')
    text_clip=text_clip.set_opacity(.3)
    text_clip=text_clip.set_duration(clip.duration)
    #Вычисляем ширину тектового клипа и самого видео
    text_width,text_height=text_clip.size
    video_width,video_height=clip.size

    # Создаем массив для хранения копий текстового клипа
    text_clips = []

    #проходим по горизонтали с шагом равным ширине текстового клипа
    for i in range(0, video_width, text_width):
    #проходим по вертикали с шагом равным ширине текстового клипа    
        for j in range(0, video_height, text_height):
            text_clips.append(text_clip.set_pos((i, j)))

    return CompositeVideoClip([clip] + text_clips)