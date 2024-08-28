from .weather import weather
from telegram import Update
from telegram.ext import  ContextTypes
from .utils import *
from .menu import menu
from .default import default
from .photo import send_photo,rotate_photo_left, rotate_photo_right,photo_menu_options, photo_boarder,photo_detail,photo_grayscale,photo_flip,photo_sepia,photo_sharpen,photo_invert,photo_noise,photo_blur
from .video import send_video,video_edit_options,slow_video,fast_video, concat_video
from .plans import plans,get_finished_plans,get_plans,delete_plan, set_plan_finished

async def menu_choice(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    
    query=update.callback_query
    await query.answer()

    if query.data=='weather':
        return await weather(update, context)
    elif query.data =='default':
        return await default(update,context)
    elif query.data =='video':
        return await video_edit_options(update,context,markup=video_markup)
    elif query.data =='plans':
        return await plans(update,context)
    elif query.data.startswith('delete'):
        return await delete_plan(update,context)
    elif query.data.startswith('mark_done'):
        return await set_plan_finished(update,context)
    elif query.data =='set_plans':
        await query.edit_message_text("Сформируйте свою новую цель")
        return SETTING_PLANS
    elif query.data=='get_plans':
        return await get_plans(update,context)
    elif query.data =='get_finished_plans':
        return await get_finished_plans(update,context)
    elif query.data =='photo':
        return await photo_menu_options(update,context,markup=photo_markup)
    
async def photo_choice(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    query=update.callback_query
    await query.answer()

    if query.data=='rotate_photo':
        return await photo_menu_options(update,context,markup=rotate_photo_markup)
    elif query.data =='rotate_photo_left':
        return await rotate_photo_left(update,context)
    elif query.data =='rotate_photo_right':
        return await rotate_photo_right(update,context)
    elif query.data =='go_back':
        return await photo_menu_options(update,context,markup=photo_markup)
    elif query.data =='send_photo':
        return await send_photo(update,context)
    elif query.data =='save_photo':
        await query.edit_message_text("Пришлите фото, которое планируете сохранить")
        return SAVING_PHOTO
    elif query.data=='photo_grayscale':
        return await photo_grayscale(update,context)
    elif query.data =='add_watermark':
        await query.edit_message_text("Пришлите надпись которую хотите наложить")
        return ADD_WATERMARK
    elif query.data=='photo_effect':
        return await photo_menu_options(update,context,markup=filter_photo_markup)
    elif query.data =='photo_blur':
        return await photo_blur(update,context)
    elif query.data == 'photo_sharpen':
        return await photo_sharpen(update,context)
    elif query.data =='photo_detail':
        return await photo_detail(update,context)
    elif query.data =='photo_flip':
        return await photo_flip(update,context)
    elif query.data =='photo_invert':
        return await photo_invert(update,context)
    elif query.data =='photo_boarder':
        return await photo_boarder(update,context)
    elif query.data =='photo_noise':
        return await photo_noise(update,context)
    elif query.data =='photo_sepia':
        return await photo_sepia(update,context)
    elif query.data =='go_back_menu':
        return await menu(update,context)

    
async def video_choice(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    
        query=update.callback_query
        await query.answer()

        if query.data=='video_cut':
            await query.edit_message_text("С какой секунды обрезать?")
            return ASK_VIDEOCUT_START
        elif query.data == 'send_video':
            return await send_video(update,context)
        elif query.data =='save_video':
            await query.edit_message_text("Пришлите видео, которое планируете сохранить")
            return SAVING_VIDEO
        elif query.data =='go_back':
            return await menu(update,context)
        elif query.data =='change_speed':
            return await video_edit_options(update,context,markup=video_speed_markup)
        elif query.data =='slow_video':
            return await slow_video(update,context)
        elif query.data =='fast_video':
            return await fast_video(update,context)
        elif query.data =='go_video_menu':
            return await video_edit_options(update,context,markup=video_markup)
        elif query.data =='add_watermark':
            await query.edit_message_text("Пришлите надпись которую хотите наложить")
            return ADD_WATERMARK_VIDEO
        elif query.data =='concat_video':
            await query.edit_message_text("Пришлите видео, которые хотите объединить")
            return CONCAT_VIDEO
    