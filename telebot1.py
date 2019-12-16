from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from handlers import *
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - $(message)s', level=logging.INFO,filename='bot.log')


def main():
    mybot = Updater(settings.BOT_API_KEY,request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('stop', bye_user, pass_user_data=True))
    dp.add_handler(CommandHandler('sith', send_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(sith)$', send_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
