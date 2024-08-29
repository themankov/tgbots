from telegram import Update
from telegram.ext import  ContextTypes
from PIL import ImageFile,ImageDraw,ImageFont,ImageFilter,ImageOps
import os
import io
import numpy as np
import asyncio
from PIL import Image
from datetime import datetime
from .utils import *
from .menu import menu


directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'photo')
async def photo_menu_options(update:Update,context:ContextTypes.DEFAULT_TYPE,markup):
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
        return PROCESS_PHOTO


async def send_photo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    if len(os.listdir(directory))==0:
        await askingInfoEdit(update, context, "Не найдено фото для отправки")
        return await menu(update,context)
    await askingInfoEdit(update, context, "Готовим фото для выгрузки")
    photo_bytes=await get_photo(update,context)
    if update.callback_query:
                    await update.callback_query.message.reply_photo(photo=photo_bytes,disable_notification=True)
    else:
                     await update.message.reply_photo(photo=photo_bytes,disable_notification=True)  
    
    await askingInfoMessage(update, context, "Все фото отправлены")
    await asyncio.sleep(3)
    
    # Возвращаем меню
    await update.callback_query.message.reply_text(
            text="Выберите действие:",
            reply_markup=menu_markup
        )
    return PROCESS_MENU
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
    return await photo_menu_options(update,context,photo_edit_markup)


def photo_edit_decorator(func):
    async def wrapper(update, context): 

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{context.user_data['name']}_{timestamp}.jpg"
        photo_bytes = await get_photo(update, context)
        delete_all_files_in_directory(directory)
        image =Image.open(io.BytesIO(photo_bytes))
        edited_photo=await func(image,update)

        # Сохраняем измененное изображение во временный файл
        temp_file_path = os.path.join(directory, file_name)
        edited_photo.save(temp_file_path)
        if update.message and update.message.text:
            await askingInfoMessage(update, context, "Изменения сохранены")
        else:
            await askingInfoEdit(update, context, "Изменения сохранены")    
        return await photo_menu_options(update,context,photo_edit_markup)
    return wrapper

@photo_edit_decorator
async def rotate_photo_left(image: ImageFile,update) -> None: 
  return  image.rotate(90)
@photo_edit_decorator
async def photo_blur(image: ImageFile,update) -> None: 
  return  image.filter(ImageFilter.BLUR)
@photo_edit_decorator
async def photo_sharpen(image: ImageFile,update) -> None: 
  return  image.filter(ImageFilter.SHARPEN)
@photo_edit_decorator
async def photo_detail(image: ImageFile,update) -> None: 
  return  image.filter(ImageFilter.DETAIL)
@photo_edit_decorator
async def photo_flip(image: ImageFile,update) -> None: 
  return  image.transpose(Image.FLIP_LEFT_RIGHT)
@photo_edit_decorator
async def photo_invert(image: ImageFile,update) -> None: 
  return  ImageOps.invert(image)
@photo_edit_decorator
async def photo_grayscale(image: ImageFile,update) -> None: 
  return  ImageOps.grayscale(image)
@photo_edit_decorator
async def photo_sepia(image: ImageFile,update) -> None: 
    sepia = []
    for i in range(256):
        r = int(i * 240 / 255)
        g = int(i * 200 / 255)
        b = int(i * 145 / 255)
        sepia.extend((r, g, b))
    
    # Разделяем изображение на каналы R, G, B
    r, g, b = image.split()
    
    # Применяем палитру сепии к каждому каналу
    r = r.point(lambda p: sepia[p * 3])
    g = g.point(lambda p: sepia[p * 3 + 1])
    b = b.point(lambda p: sepia[p * 3 + 2])
    
    # Объединяем каналы обратно
    return Image.merge("RGB", (r, g, b))
@photo_edit_decorator
async def photo_noise(image: ImageFile,update) -> None: 
    noise = np.random.normal(0, 25, (image.height, image.width, 3)).astype(np.uint8)
    noisy_image = np.array(image) + noise
    noisy_image = Image.fromarray(np.clip(noisy_image, 0, 255).astype(np.uint8))
    return noisy_image
@photo_edit_decorator
async def photo_boarder(image: ImageFile,update) -> None: 
  return  ImageOps.expand(image, border=20, fill='black')
@photo_edit_decorator
async def rotate_photo_right(image: ImageFile,update) -> None: 
  return  image.rotate(-90)
@photo_edit_decorator
async def add_watermark(image,update) -> None: 
    
    watermark_text=update.message.text
    # Создаем прозрачный слой по размерам идентичный фото,каждый пиксель поддерживает rgba
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    #получаем объект с методами для рисования по прозрачному слою
    draw = ImageDraw.Draw(txt)
    # Настройка шрифта и размера текста
    font = ImageFont.truetype('arial.ttf', 36)

    # Определение прямоугольник, где будет расположен текст
    textbbox = draw.textbbox((0, 0), watermark_text, font=font)
    #(x0, y0, x1, y1) -верхний левый, нижний правый угол
    textwidth, textheight = textbbox[2] - textbbox[0], textbbox[3] - textbbox[1]

    y = image.height - textheight - 10
    while y > -1000:
        x = image.width - textwidth - 10
        while x > -1000:
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 130))
            x -= textwidth + 10
        y -= textheight + 10   

    # Объединение водяного знака с оригинальным изображением, которое сначала конвертируется в rgba как и слой прозрачный
    watermarked = Image.alpha_composite(image.convert('RGBA'), txt)
    #это для форматов, которые не поддерживают прозрачность (jpeg)
    watermarked = watermarked.convert("RGB")
    await update.message.reply_text('Почти готово...')
    return watermarked    




async def get_photo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    photo=None
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            with open(file_path, 'rb') as photo:
                photo=photo
                photo_bytes=photo.read()
    return photo_bytes

