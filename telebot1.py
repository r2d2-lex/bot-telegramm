from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

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
    update.message.reply_text(text, reply_markup=get_keyboard())


def bye_user(bot, update, user_data):
    text = 'Вызван STOP!'
    print(text)
    #update.message.reply_text(text)
    bot.send_message(chat_id=update.message.chat_id, text='Stop', reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Привет {0} {1}! Ты написал: {2}".format(update.message.chat.first_name, emo,
                                                         update.message.text)
    logging.info("User %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    print(update.message)
    print('Date:',update.message['date'])
    print('From:', update.message['chat']['first_name'], update.message['chat']['last_name'])
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def send_picture(bot, update, user_data):
    img_dir = "sith"
    img_list = glob(img_dir+"/*.jp*g")
    img_pic = choice(img_list)
    bot.send_photo(chat_id=update.message.chat_id,photo=open(img_pic,'rb'), reply_markup=get_keyboard())


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text("Готово {}".format(get_user_emo(user_data)), reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text("Готово {}".format(get_user_emo(user_data)), reply_markup=get_keyboard())


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)

    my_keyboard = ReplyKeyboardMarkup([['start', 'stop', '/sith'],
                                       [contact_button, location_button]])
    return(my_keyboard)

def main():
    mybot = Updater(settings.API_KEY,request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('stop', bye_user, pass_user_data=True))
    dp.add_handler(CommandHandler('sith', send_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(sith)$', send_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
