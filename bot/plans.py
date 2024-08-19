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
    await askingInfoMessage(update,context,'Ваша цель успешно сформирована. Удачи!')
    return await menu(update,context)
async def get_finished_plans(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    username,userId=await isUserExist(update,context)
    finishedPlans=session.query(Plan).filter(Plan.userId==userId).filter(Plan.finished==True).all()
    if len(finishedPlans)==0:
         await askingInfoMessage(update,context,'Завершенных целей не найдено') 
    await askingInfoEdit(update,context,"Ваши завершенные цели:")
    for i in range(len(finishedPlans)):
        await askingInfoMessage(update,context,"✅ "+finishedPlans[i].content)  
    await update.callback_query.message.reply_text(
            text="Выберите действие:",
            reply_markup=menu_markup
        )                

async def get_plans(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    username,userId=await isUserExist(update,context)
    plans=session.query(Plan).filter(Plan.userId==userId).filter(Plan.finished==False).all()
    if len(plans)==0:
        await askingInfoEdit(update,context,"Цели не заданы")
        await asyncio.sleep(4)
        return await menu(update,context)
    # Создание клавиатуры с кнопками для каждого плана
    keyboard = []
    for plan in plans:
        keyboard.append([InlineKeyboardButton(plan.content, callback_data=f"plan_{plan.id}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text("Ваши планы:", reply_markup=reply_markup)
    elif update.message:
        await update.message.edit_text("Ваши планы:", reply_markup=reply_markup)   
    return MARK_PLAN  

async def mark_plan(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    query = update.callback_query
    await query.answer()
    
    # Получаем ID плана из callback_data
    plan_id = int(query.data.split("_")[-1])

    # Предлагаем пользователю действия с этим планом
    keyboard = [
        [InlineKeyboardButton("Пометить как завершённый", callback_data=f"mark_done_{plan_id}")],
        [InlineKeyboardButton("Удалить", callback_data=f"delete_{plan_id}")],
        [InlineKeyboardButton("Отменить", callback_data='plans')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text="Выберите действие", reply_markup=reply_markup)  
    return PROCESS_MENU

async def delete_plan(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    query = update.callback_query
    await query.answer()
    
    plan_id = query.data.split("_")[1]
    plan_id = int(plan_id)
    session.query(Plan).filter(Plan.id==plan_id).delete(synchronize_session='fetch')
    session.commit()
    return await plans(update,context)

async def set_plan_finished(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    query = update.callback_query
    await query.answer()
    
    plan_id = query.data.split("_")[2]
    plan_id = int(plan_id)
    session.query(Plan).filter(Plan.id==plan_id).update({"finished":True})
    session.commit()
    return await get_plans(update,context)