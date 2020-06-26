from glob import glob
from random import choice
from utils import get_keyboard, is_sword
from telegram import error, ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
import os
import logging
from telebot1 import subscribers
from db import db, get_or_create_user, get_user_emo, toggle_subscription, get_subscribers
from telegram.ext import messagequeue as mq


def anketa_start(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text('Как вас зовут? Напишите имя и фамилию', reply_markup=ReplyKeyboardRemove())
    return "name"


def anketa_get_name(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
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
    user = get_or_create_user(db, update.effective_user, update.message)
    user_data['anketa_rating'] = update.message.text
    update.message.reply_text("""Пожалуйста напишите отзыв в свободной форме 
        или /skip что пропустить этот шаг""")
    return "comment"


def anketa_comment(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    user_data['anketa_comment'] = update.message.text
    user_text = """
    <b>Имя Фамилия:</b> {anketa_name}
    <b>Оценка:</b> {anketa_rating}
    <b>Коментарий:</b> {anketa_comment}
    """.format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_skip_comment(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    user_text = """
      <b>Имя Фамилия:</b> {anketa_name}
      <b>Оценка:</b> {anketa_rating}
      """.format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def change_avatar(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    if 'emo' in user:
        del user['emo']
    emo = get_user_emo(db, user)
    update.message.reply_text('Готово {}'.format(emo), reply_markup=get_keyboard())


def dont_known(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text("Я не понимаю")
    return


def greet_user(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    #debug
    print("User:", user)
    print("user_data:", user_data)
    print("Effective User: ", update.effective_user, "\r\n")
    print("Update Message: ", update.message, "\r\n")
    #/debug
    emo = get_user_emo(db, user)
    user_data['emo'] = emo

    text = 'Вызван start!'
    print(text)
    update.message.reply_text(text, reply_markup=get_keyboard())


def bye_user(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    text = 'Вызван STOP!'
    print(text)
    bot.send_message(chat_id=update.message.chat_id, text='Stop', reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    emo = get_user_emo(db, user)
    user_text = "Привет {0} {1}! Ты написал: {2}".format(user['first_name'], emo,
                                                         update.message.text)
    logging.info("User %s, Chat id: %s, Message: %s", user['first_name'],
                 update.message.chat_id, update.message['text'])
    # print(update.message)
    print('Date:', update.message['date'])
    print('From:', update.message['chat']['first_name'], update.message['chat']['last_name'])
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def send_picture(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    img_dir = "sith"
    img_list = glob(img_dir + "/*.jp*g")
    img_pic = choice(img_list)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(img_pic, 'rb'), reply_markup=get_keyboard())


def get_contact(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    print(update.message.contact)
    update.message.reply_text("Готово {}".format(get_user_emo(db, user)), reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
    print(update.message.location)
    update.message.reply_text("Готово {}".format(get_user_emo(db, user)), reply_markup=get_keyboard())


def check_user_photo(bot, update, user_data):
    user = get_or_create_user(db, update.effective_user, update.message)
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


def subscribe(bot, update):
    user = get_or_create_user(db, update.effective_user, update.message)
    if not user.get('subscribed'):
        toggle_subscription(db, user)
    update.message.reply_text('Вы подписались')
    #print(subscribers)


@mq.queuedmessage
def send_updates(bot, job):
    for user in get_subscribers(db):
        try:
            bot.send_message(chat_id=user['chat_id'], text='Auto messages...')
        except error.BadRequest:
            print ('Чат {}, не найден'.format(user['chat_id']))


def unsubscribe(bot, update):
    user = get_or_create_user(db, update.effective_user, update.message)
    if user.get('subscribed'):
        toggle_subscription(db, user)
        update.message.reply_text('Вы отписались')
    else:
        update.message.reply_text('Вы не подписаны, нажмите /subscribe чтобы подписаться')


def set_alarm(bot, update, args, job_queue):
    user = get_or_create_user(db, update.effective_user, update.message)
    try:
        seconds = abs(int(args[0]))
        job_queue.run_once(alarm, seconds, context=update.message.chat_id)
    except (IndexError, ValueError):
        update.message.reply_text('Введите число после команды /alarm')


# @mq.queuedmessage
def alarm(bot, job):
    bot.send_message(chat_id=job.context, text="Сработал будильник")
