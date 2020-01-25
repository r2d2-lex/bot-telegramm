from glob import glob
from random import choice
from utils import get_keyboard, get_user_emo, is_sword
from telegram import ParseMode
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
import os
import logging


def anketa_start(bot, update, user_data):
    update.message.reply_text('Как вас зовут? Напишите имя и фамилию', reply_markup=ReplyKeyboardRemove())
    return "name"


def anketa_get_name(bot, update, user_data):
    username = update.message.text
    if len(username.split(" ")) != 2:
        update.message.reply_text("Пожалуйста введите имя и фамилию")
        return "name"
    else:
        user_data['anketa_name'] = username
        reply_keyboard = [["1", "2", "3", "4", "5"]]
        update.message.reply_text(
            "Оцените нашего бота от 1 до 5",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return "rating"


def anketa_rating(bot, update, user_data):
    user_data['anketa_rating'] = update.message.text
    update.message.reply_text("""Пожалуйста напишите отзыв в свободной форме 
        или /skip что пропустить этот шаг""")
    return "comment"


def anketa_comment(bot, update, user_data):
    user_data['anketa_comment'] = update.message.text
    user_text = """
    <b>Имя Фамилия:</b> {anketa_name}
    <b>Оценка:</b> {anketa_rating}
    <b>Коментарий:</b> {anketa_comment}
    """.format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_skip_comment(bot, update, user_data):
    user_text = """
      <b>Имя Фамилия:</b> {anketa_name}
      <b>Оценка:</b> {anketa_rating}
      """.format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def dont_known(bot, update, user_data):
    update.message.reply_text("Я не понимаю")
    return


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


def check_user_photo(bot, update, user_data):
    update.message.reply_text("Обработка фото...")
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', 'sword_{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    if is_sword(filename):
        update.message.reply_text("Обнаружен меч, добавляю в библиотеку")
        new_filename = os.path.join('sith', 'sword_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Меч не обнаружен!")