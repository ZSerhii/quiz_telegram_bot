import logs
import handlers
from os import path
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters


CURRENT_PATH = path.dirname(path.abspath(__file__)) + '\\'


with open(CURRENT_PATH + '.token') as token:
    TELEGRAM_TOKEN = token.read()


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start',  handlers.handle_start))
    updater.dispatcher.add_handler(CommandHandler('help',   handlers.handle_help))
    updater.dispatcher.add_handler(CallbackQueryHandler(handlers.handle_button))
    updater.dispatcher.add_handler(CommandHandler('next',   handlers.handle_next))
    updater.dispatcher.add_handler(CommandHandler('get',    handlers.handle_get))
    updater.dispatcher.add_handler(CommandHandler('finish', handlers.handle_finish))
    updater.dispatcher.add_handler(CommandHandler('result', handlers.handle_result))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handlers.echo))
    updater.dispatcher.add_error_handler(logs.handler_error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
