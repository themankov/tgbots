#Любое обновление бота через телеграм(содержит в себе все данные об обнове (текст сообщения,инфа о пользователе))
from telegram import Update
#ApplicationBuilder-создание экземпляра бота, настройка его компонентов
#CommandHandler-обработка комманд(/help,/start)
#ContextTypes-хранение контекста(DEFAULT_TYPE-инфа о чате, пользователе)
#MessageHandler-обработка любых тектовых сообщений, что не команды
#filters-модуль фильтров для сообщений(распознавать текстовые или команднве сообщения)
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

async def start (update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    name=context.user_data.get('name',None)
    color=context.user_data.get('color',None)
    if bool(color) and bool(name) :
        await update.message.reply_text(f'Привет {name}, я помню, твой любимый цвет - {color}')
    else:
        await update.message.reply_text('What is your name?')
        context.user_data['state']='ASKING NAME'
     
    
    
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("\n/hello - Say hello\n/help - List commands")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = context.user_data.get('state')

    if state == 'ASKING NAME':
        context.user_data['name'] = update.message.text
        await update.message.reply_text(f"Приятно познакомиться, {context.user_data['name']}! Какой твой любимый цвет?")
        context.user_data['state']='ASKING COLOR'
        
    elif state == 'ASKING COLOR':
        context.user_data['color'] = update.message.text
        await update.message.reply_text(f"Отлично! Я запомню, что твой любимый цвет — {context.user_data['color']}.")
        context.user_data['state'] = None
    else:
        await update.message.reply_text("Вы можете начать с /start.")
app = ApplicationBuilder().token("6867300294:AAEXa-svt9_x3Yt7q66tOAcCwYkPmBNLQwY").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
