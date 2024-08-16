from telegram.ext import  CommandHandler,  MessageHandler, filters, ConversationHandler,CallbackQueryHandler
from .utils import *
from .processingData import menu_choice
from .default import confirm_delete,delete_data
from .questions import ask_color,ask_name,processing_city, start
from .video import save_video
from .photo import save_photo

cnv_handler=ConversationHandler(
    entry_points=[CommandHandler('start',start)],
    states={
        ASK_NAME:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_name)],
        ASK_COLOR:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_color)],
        PROCESS_CITY:[CallbackQueryHandler(processing_city)],
        PROCESS_DELETE_CONFIRMATION1:[CallbackQueryHandler(confirm_delete)],
        PROCESS_DELETE_CONFIRMATION2:[CallbackQueryHandler(delete_data)],
        PROCESS_MENU:[CallbackQueryHandler(menu_choice)],
        SAVING_PHOTO:[MessageHandler(filters.PHOTO,save_photo)],
        SAVING_VIDEO:[MessageHandler(filters.VIDEO,save_video)],
    },
    per_message=False,
    fallbacks=[CommandHandler('start',start)])