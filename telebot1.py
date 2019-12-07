from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

from random import choice
from glob import glob
from emoji import emojize

import logging
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - $(message)s', level=logging.INFO,filename='bot.log')

def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo

    text = 'Вызван start!'
    print(text)
    bot.send_message(chat_id=update.message.chat_id, text='Hi! nigga')


def bye_user(bot, update, user_data):
    text = 'Вызван STOP!'
    print(text)
    my_keyboard = ReplyKeyboardMarkup([['Yes', 'No']])
    update.message.reply_text(text,reply_markup = my_keyboard)
    #update.message.reply_text(text)


def talk_to_me(bot, update, user_data):
    user_text = "Привет {0} {1}! Ты написал: {2}".format(update.message.chat.first_name,user_data['emo'],
                                                         update.message.text)
    logging.info("User %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    print(update.message)
    print('Date:',update.message['date'])
    print('From:', update.message['chat']['first_name'], update.message['chat']['last_name'])
    update.message.reply_text(user_text)


def send_picture(bot, update, user_data):
    img_dir = "sith"
    img_list = glob(img_dir+"/*.jp*g")
    img_pic = choice(img_list)
    bot.send_photo(chat_id=update.message.chat_id,photo=open(img_pic,'rb'))

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']

def main():
    mybot = Updater(settings.API_KEY,request_kwargs=settings.PROXY)
    # Из за этой строчки не работало...
    #use_context=True

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('stop', bye_user, pass_user_data=True))
    dp.add_handler(CommandHandler('sith', send_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
