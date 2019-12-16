from glob import glob
from random import choice
from utils import get_keyboard, get_user_emo
import logging

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


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text("Готово {}".format(get_user_emo(user_data)), reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text("Готово {}".format(get_user_emo(user_data)), reply_markup=get_keyboard())
