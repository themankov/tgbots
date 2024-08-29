from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import  ContextTypes
from .utils import *
from .questions import start
import asyncio
from .database import async_session, User
from .menu import menu

async def default(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    keyboard=[
        [InlineKeyboardButton('Удалить все данные', callback_data='delete_data')] 
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
            await update.callback_query.edit_message_text("Выберите действие",reply_markup=markup)
    else:
            await update.message.edit_text("Выберите действие",reply_markup=markup)
    return PROCESS_DELETE_CONFIRMATION1

async def delete_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username,userId=await isUserExist(update,context)
    query = update.callback_query
    await query.answer()

    if query.data=='delete':
        # Удаление из папок
        directory1 = os.path.join(os.path.dirname(__file__), '..', 'data', 'photo')
        directory2 = os.path.join(os.path.dirname(__file__), '..', 'data', 'video')
        for i in map(delete_all_files_in_directory,[directory1,directory2]):
             continue
        context.user_data.clear()
        async with async_session() as session:
             
            await session.query(User).delete(synchronize_session='fetch')
            await query.edit_message_text("Все данные успешно удалены.")
        
    elif query.data=='cancel':   
         await query.edit_message_text("Удаление отменено.")
    return await start(update,context)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Удаление отменено") 
