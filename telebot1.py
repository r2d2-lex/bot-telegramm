from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, RegexHandler
from telegram.ext import messagequeue as mq
from handlers import *
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - $(message)s', level=logging.INFO, filename='bot.log')

subscribers = set()


def main():
    mybot = Updater(settings.BOT_API_KEY,request_kwargs=settings.PROXY)
    mybot.bot._msg_queue = mq.MessageQueue
    mybot.bot._is_messages_queued_default = True

    dp = mybot.dispatcher

    mybot.job_queue.run_repeating(send_updates, interval=5)

    anketa = ConversationHandler(
        entry_points=[RegexHandler('^(Заполнить анкету)$', anketa_start, pass_user_data=True)],
        states={
            "name" : [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
            "rating" : [RegexHandler('^(1|2|3|4|5)$', anketa_rating, pass_user_data=True)],
            "comment" : [MessageHandler(Filters.text|Filters.photo|Filters.video|Filters.document,
                                        anketa_comment, pass_user_data=True),
                         CommandHandler('skip', anketa_skip_comment, pass_user_data=True)],
        },
        fallbacks=[MessageHandler(Filters.text, dont_known, pass_user_data=True)]
    )

    dp.add_handler(CommandHandler('alarm', set_alarm, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('stop', bye_user, pass_user_data=True))
    dp.add_handler(CommandHandler('sith', send_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(sith)$', send_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватар)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    # Last in handlers...
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
