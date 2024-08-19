from telegram import Update
from telegram.ext import  ContextTypes
import os
import asyncio
from .database import Plan,session
from datetime import datetime
from .utils import *
from .menu import menu

async def plans(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    markup = plans_markup

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
    return PROCESS_MENU

async def set_plans(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    text = update.message.text
    username,userId=await isUserExist(update,context)
    new_plan = Plan(date=datetime.now().strftime("%Y%m%d"), content=text, finished=False, userId=int(userId))
    session.add(new_plan)
    session.commit()
    await askingInfoEdit(update,context,'Ваша цель успешно сформирована. Удачи!')
    return await menu(update,context)
async def get_finished_plans(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    username,userId=await isUserExist(update,context)
    finishedPlans=session.query(Plan).filter(Plan.userId==userId).filter(Plan.finished==True).all()
    if len(finishedPlans)==0:
         await askingInfoMessage('Завершенных целей не найдено') 
    await askingInfoEdit(update,context,"Ваши завершенные цели:")
    for i in range(len(finishedPlans)):
        await askingInfoMessage("✅ "+finishedPlans[i].content)  
    await update.callback_query.message.reply_text(
            text="Выберите действие:",
            reply_markup=menu_markup
        )                
      