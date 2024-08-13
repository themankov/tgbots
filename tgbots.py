#Любое обновление бота через телеграм(содержит в себе все данные об обнове (текст сообщения,инфа о пользователе))
from telegram import Update
#ApplicationBuilder-создание экземпляра бота, настройка его компонентов
#CommandHandler-обработка комманд(/help,/start)
#ContextTypes-хранение контекста(DEFAULT_TYPE-инфа о чате, пользователе)
#MessageHandler-обработка любых тектовых сообщений, что не команды
#filters-модуль фильтров для сообщений(распознавать текстовые или команднве сообщения)
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

ASK_NAME,ASK_COLOR, WAITING_FOR_COMMAND=range(3)
async def start (update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    name=context.user_data.get('name',None)
    color=context.user_data.get('color',None)
    if bool(color) and bool(name) :
        await update.message.reply_text(f'Привет {name}, я помню, твой любимый цвет - {color}')
        return WAITING_FOR_COMMAND
    else:
        await update.message.reply_text('What is your name?')
        return ASK_NAME
     
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f"Приятно познакомиться, {context.user_data['name']}! Какой твой любимый цвет?")
    return ASK_COLOR
async def ask_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['color'] = update.message.text
    await update.message.reply_text(f"Отлично! Я запомню, что твой любимый цвет — {context.user_data['color']}.")
    return WAITING_FOR_COMMAND
async def default(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    context.user_data.clear()
    await update.message.reply_text('Данные очищены')
    return await start(update, context)
async def waiting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Я жду ваших команд. Вы можете использовать /default для сброса данных.")
    return WAITING_FOR_COMMAND
async def cancel(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:
    await update.message.reply_text('Диалог завершен')
    return ConversationHandler.END     
cnv_handler=ConversationHandler(
    entry_points=[CommandHandler('start',start)],
    states={
        ASK_NAME:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_name)],
        ASK_COLOR:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_color)],
        WAITING_FOR_COMMAND:[MessageHandler(filters.TEXT and ~filters.COMMAND,waiting)]
    },
    fallbacks=[CommandHandler('cancel',cancel),CommandHandler('default',default)]
)    
app = ApplicationBuilder().token("6867300294:AAEXa-svt9_x3Yt7q66tOAcCwYkPmBNLQwY").build()
app.add_handler(cnv_handler)
app.run_polling()
