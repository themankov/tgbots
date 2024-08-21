from .weather import weather
from telegram import Update
from telegram.ext import  ContextTypes
from .utils import *
from .default import default
from .photo import send_photo,photo,edit_photo,rotate_options_photo,rotate_photo
from .video import send_video,video
from .plans import plans,get_finished_plans,get_plans,delete_plan, set_plan_finished

async def menu_choice(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    
    query=update.callback_query
    await query.answer()

    if query.data=='weather':
        return await weather(update, context)
    elif query.data =='default':
        return await default(update,context)
    elif query.data =='photo':
        return await photo(update,context)
    elif query.data =='video':
        return await video(update,context)
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
    elif query.data == 'send_video':
        return await send_video(update,context)
    elif query.data =='send_photo':
        return await send_photo(update,context)
    elif query.data =='save_photo':
        await query.edit_message_text("Пришлите фото, которое планируете сохранить")
        return SAVING_PHOTO
    elif query.data =='save_video':
        await query.edit_message_text("Пришлите видео, которое планируете сохранить")
        return SAVING_VIDEO
    
async def photo_choice(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    query=update.callback_query
    await query.answer()

    if query.data=='rotate_photo':
        return await rotate_photo(update,context)
    elif query.data.startswith('rotate_photo_'):
        return await rotate_options_photo(update,context)
    elif query.data =='go_back':
        return await photo(update,context)
    elif query.data =='video':
        return await video(update,context)
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
    elif query.data == 'send_video':
        return await send_video(update,context)
    elif query.data =='send_photo':
        return await send_photo(update,context)
    elif query.data =='save_photo':
        await query.edit_message_text("Пришлите фото, которое планируете сохранить")
        return SAVING_PHOTO
    elif query.data =='save_video':
        await query.edit_message_text("Пришлите видео, которое планируете сохранить")
        return SAVING_VIDEO