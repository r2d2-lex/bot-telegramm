from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - $(message)s', level=logging.INFO,filename='bot.log')

def greet_user(bot,update):
    text = 'Вызван start!'
    print(text)
    bot.send_message(chat_id=update.message.chat_id, text='Hi! nigga')

def bye_user(bot,update):
    text = 'Вызван STOP!'
    print(text)
    update.message.reply_text(text)

def talk_to_me(bot,update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def main():
    mybot = Updater(settings.API_KEY,request_kwargs=settings.PROXY)
    # Из за этой строчки не работало...
    #use_context=True

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('stop', bye_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()