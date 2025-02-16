from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import  ContextTypes
from .utils import *
from .menu import menu
from .video import cut
from sqlalchemy.future import select
from .database import User,async_session

async def start (update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    username,userId=await isUserExist(update,context)
    user=None
    if username is None:
        await update.message.reply_text('Перед использованием бота вам необходимо установить username')
        return ConversationHandler.END
    async with async_session() as session:
        user= await session.execute(select(User).filter_by(userId=userId))
        user=user.scalars().first()
        if user is None:
            await askingInfoMessage(update,context,'Привет, Придумай себе пользовательское имя')
            return ASK_NAME
        elif username!=user.username:
            await update.message.reply_text('Похоже раньше вы использовали другой ник в телеграмме.Удалить прошлые данные?')
            return await confirm_delete(update,context)
        elif user :
            context.user_data['name']=user.name
            context.user_data['age']=user.age
            context.user_data['city']=user.city
            return await menu(update,context)
        # Возвращаем меню
        #  if update.callback_query:
        #     await update.callback_query.edit_message_text(
        #         text="Выберите действие:",
        #         reply_markup=menu_markup)
        #  elif update.message:
        #     await update.message.reply_text(
        #         text="Выберите действие:",
        #         reply_markup=menu_markup)  
            
            

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await askingInfoMessage(update,context,'Сколько тебе лет?')
    return ASK_AGE

async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
         age = update.message.text
         if str.isnumeric(age)==False :
             await update.message.reply_text('Возраст должен быть целым числом.Попробуйте снова')
             return ASK_AGE
         context.user_data['age'] = update.message.text
         return await ask_city(update,context)

async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Москва", callback_data='Москва')],
        [InlineKeyboardButton("Санкт-Петербург", callback_data='Санкт-Петербург')],
        [InlineKeyboardButton('Волгоград',callback_data='Волгоград')]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите город",reply_markup=markup)
    return PROCESS_CITY
async def processing_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    context.user_data['city'] = query.data
    await storeInfoDB(update,context)
    return await menu(update,context)   

async def storeInfoDB(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    username,userId=await isUserExist(update,context)
    
    name=context.user_data['name']
    age=context.user_data['age']
    city=context.user_data['city']
    async with async_session() as session:
     async with session.begin(): 
        new_user= User(userId=int(userId),username=username,name=name,age=int(age),city=city)
        await session.add(new_user)
        await session.commit()
async def confirm_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [
        [InlineKeyboardButton("Да", callback_data='delete')],
        [InlineKeyboardButton("Нет", callback_data='cancel')],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.edit_message_text("Вы уверены, что хотите удалить все данные?", reply_markup=markup)
    elif update.message:
        await update.message.edit_text("Вы уверены, что хотите удалить все данные?", reply_markup=markup)
    return PROCESS_DELETE_CONFIRMATION2  
async def ask_video_start(update:Update,context:ContextTypes.DEFAULT_TYPE):
     context.user_data['start']=update.message.text
     await askingInfoMessage(update,context,'До какой секунды обрезать?')
     return ASK_VIDEOCUT_END
async def ask_video_end(update:Update,context:ContextTypes.DEFAULT_TYPE):
     context.user_data['end']=update.message.text
     return await cut(update,context)