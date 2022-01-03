#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

import psycopg2.errors
import sqlalchemy.exc
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
from app import submit, delete

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

def remove(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    '''    try:
        delete(str(user.id))
    except Exception as e:
        print("exception is - " + str(e))
        print(type(e))
        update.message.reply_markdown_v2(
            'Error occured\.\n'
            # reply_markup=ForceReply(selective=True),
        )
        return'''
    delete(str(user.id))
    update.message.reply_markdown_v2(
        'You are now removed\.\n'
        # reply_markup=ForceReply(selective=True),
    )


def register(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    try:
        submit(str(user.id), user.name)
    except sqlalchemy.exc.IntegrityError as e:
        print("exception is - " + str(e))
        print(type(e))
        update.message.reply_markdown_v2(
            'Error occured\.\n You are already registred to the system\.\n'
            # reply_markup=ForceReply(selective=True),
        )
        return
    except Exception as e:
        print("exception is - " + str(e))
        print(type(e))
        update.message.reply_markdown_v2(
            'Error occured\.\n'
            # reply_markup=ForceReply(selective=True),
        )
        return
    update.message.reply_markdown_v2(
        'You are now registered\.\n'
        # reply_markup=ForceReply(selective=True),
    )


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hello, {user.mention_markdown_v2()}\!'
        # reply_markup=ForceReply(selective=True),
    )

    update.message.reply_markdown_v2(
        'Welcome to smart polling\.\n'
        'Please choose one of the options:'
        # reply_markup=ForceReply(selective=True),
    )

    update.message.reply_markdown_v2(
        '/register \- Register to start answering polls via telegram in smart polling system\n'
        '/remove \- To stop getting polls queries\n in smart polling system\n'
        '/start \- Use start anytime to see this menu again'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5029169709:AAHvskSVaIUTmMDeJW-6XBoOzi-IC4naEjA")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
