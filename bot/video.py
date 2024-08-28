from telegram import Update
from telegram.ext import  ContextTypes
import os
from datetime import datetime
from .utils import *
from .menu import menu
from moviepy.video.fx.all import resize
from moviepy.editor import VideoFileClip,TextClip,CompositeVideoClip, concatenate_videoclips,vfx
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
# Словарь для временного хранения видео из медиа-группы
media_group_storage = {}    
async def concat_video(update:Update,context):
    media_group_id = update.message.media_group_id

    # Если это новое медиа-групповое сообщение, создаем список для хранения видео
    if media_group_id not in media_group_storage:
        media_group_storage[media_group_id] = []

    # Получаем файл видео и добавляем в список
    video_file = await update.message.video.get_file()
    media_group_storage[media_group_id].append(video_file.file_path)

    # Установим небольшую задержку, чтобы дождаться получения всех частей медиа-группы
    await asyncio.sleep(1)

    # Проверим, получены ли все части медиа-группы (ожидается 2 видео)
    if len(media_group_storage[media_group_id]) == 2:  # измените число на ожидаемое количество видео
        await askingInfoMessage(update,context,'Загрузили второе видео...')
        video_files = media_group_storage.pop(media_group_id)

        # Обрабатываем видеофайлы
        clips = []
        for i,file_path in enumerate(video_files):
           
            clip = VideoFileClip(file_path)
            path=os.path.join(directory, f"clip_{i}.mp4")
            clip.write_videofile(path, codec="libx264", audio_codec="aac", preset="slow", fps=30)
            clips.append(clip)
        final_clips=[]
        for i in range(len(clips)):
             path=os.path.join(directory, f"clip_{i}.mp4")
             final_clips.append(VideoFileClip(path))
        final_video = concatenate_videoclips(final_clips,method="compose")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{context.user_data['name']}_{timestamp}.mp4"
        video_path = os.path.join(directory, file_name)
        final_video.write_videofile(video_path)
        final_video.close()

        await update.message.reply_text("Ваше видео готово!")
        return await video_edit_options(update, context, markup=video_markup)
    await askingInfoMessage(update,context,'Загрузили одно видео...')
    
