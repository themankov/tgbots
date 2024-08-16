from telegram.ext import ApplicationBuilder
from .utils import *
from .config import TOKEN
from .handlers import cnv_handler

def init_bot():
  app = ApplicationBuilder().token(TOKEN).build()
  app.add_handler(cnv_handler)
  app.run_polling()

