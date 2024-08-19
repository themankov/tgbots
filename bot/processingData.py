from .weather import weather
from telegram import Update
from telegram.ext import  ContextTypes
from .utils import *
from .default import default
from .photo import send_photo,photo
from .video import send_video,video
from .plans import plans,set_plans,get_finished_plans

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
    elif query.data =='set_plans':
        await query.edit_message_text("Сформируйте свою новую цель")
        return SETTING_PLANS
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