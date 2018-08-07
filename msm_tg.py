import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job, MessageHandler, Filters, RegexHandler, ConversationHandler
from db import get_unposted
from db import update_posted
from msm import getPageData
from msm import parsePageData
from cfg import CHANNEL_ID
from cfg import BOT_TOKEN

def callback_minute(bot, job):
    unposted = get_unposted()
    print("Attempting to post")
    if not unposted:
        print("Nothing to post")
        pass
    else:
        for post in unposted:
            bot.send_message(chat_id=CHANNEL_ID, 
                   text=post[0])
            update_posted(post[2])
        print("message posted")

def callback_five(bot,job):
    driver = getPageData()
    parsePageData(driver) #enqueues the rip

def Bishop():
    print("Bishop Online")
    updater = Updater(token=BOT_TOKEN)
    j = updater.job_queue
    dispatcher = updater.dispatcher
    job_minute = j.run_repeating(callback_minute,interval = 60, first = 0)
    job_five = j.run_repeating(callback_five,interval = 300, first = 0)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    Bishop()