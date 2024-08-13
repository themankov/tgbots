#Любое обновление бота через телеграм(содержит в себе все данные об обнове (текст сообщения,инфа о пользователе))
from telegram import Update
#ApplicationBuilder-создание экземпляра бота, настройка его компонентов
#CommandHandler-обработка комманд(/help,/start)
#ContextTypes-хранение контекста(DEFAULT_TYPE-инфа о чате, пользователе)
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import re

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("/start - Welcome message\n/hello - Say hello\n/help - List commands")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()

    if "привет" in text:
        await update.message.reply_text("Привет! Как дела?")
    elif "пока" in text:
        await update.message.reply_text("До встречи!")
    elif re.search(r'\d+', text):
        await update.message.reply_text("Вы упомянули число!")
    else:
        await update.message.reply_text(f"Вы сказали: {update.message.text}")

app = ApplicationBuilder().token("6867300294:AAEXa-svt9_x3Yt7q66tOAcCwYkPmBNLQwY").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()