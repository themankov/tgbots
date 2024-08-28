from telegram.ext import  CommandHandler,  MessageHandler, filters, ConversationHandler,CallbackQueryHandler
from .utils import *
from .processingData import menu_choice, photo_choice,video_choice
from .default import delete_data
from .questions import ask_age,ask_name,processing_city, start, confirm_delete,ask_video_start,ask_video_end
from .video import save_video,add_watermark as add_watermark_video, concat_video
from .photo import save_photo, add_watermark
from .plans import set_plans,mark_plan

cnv_handler=ConversationHandler(
    entry_points=[CommandHandler('start',start)],
    states={
        ASK_NAME:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_name)],
        ASK_AGE:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_age)],
        PROCESS_CITY:[CallbackQueryHandler(processing_city)],
        PROCESS_DELETE_CONFIRMATION1:[CallbackQueryHandler(confirm_delete)],
        PROCESS_DELETE_CONFIRMATION2:[CallbackQueryHandler(delete_data)],
        MARK_PLAN:[CallbackQueryHandler(mark_plan)],
        PROCESS_MENU:[CallbackQueryHandler(menu_choice)],
        PROCESS_PHOTO:[CallbackQueryHandler(photo_choice)],
        PROCESS_VIDEO:[CallbackQueryHandler(video_choice)],
        ADD_WATERMARK:[MessageHandler(filters.TEXT and ~filters.COMMAND,add_watermark)],
        ADD_WATERMARK_VIDEO:[MessageHandler(filters.TEXT and ~filters.COMMAND,add_watermark_video)],
        CONCAT_VIDEO:[MessageHandler(filters.TEXT and ~filters.COMMAND,concat_video)],
        SETTING_PLANS:[MessageHandler(filters.TEXT and ~filters.COMMAND,set_plans)],
        SAVING_PHOTO:[MessageHandler(filters.PHOTO,save_photo)],
        SAVING_VIDEO:[MessageHandler(filters.VIDEO,save_video)],
        ASK_VIDEOCUT_START:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_video_start)],
        ASK_VIDEOCUT_END:[MessageHandler(filters.TEXT and ~filters.COMMAND,ask_video_end)],
    },
    per_message=False,
    fallbacks=[CommandHandler('start',start)])