from telegram.ext import ApplicationBuilder
from .utils import *
from flask import Flask, request
from .config import TOKEN
from .handlers import cnv_handler

# Инициализация Flask-приложения
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Получаем данные от Telegram
    update = request.get_json()
    # Передаем их для обработки вашим хендлерам
    application = ApplicationBuilder().token(TOKEN).build()
    application.process_update(update)
    return 'ok', 200

def init_bot():
  app = ApplicationBuilder().token(TOKEN).build()
  app.bot.set_webhook(url='http://127.0.0.1:4040') 
   # Добавляем обработчики
  app.bot.add_handler(cnv_handler)

    # Запускаем Flask-приложение
  app.run(port=8443)

