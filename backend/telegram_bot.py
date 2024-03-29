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
from telegram import (Poll, ParseMode, KeyboardButton, KeyboardButtonPollType,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot, )
from telegram.ext import Updater, CommandHandler,PollAnswerHandler, PollHandler, \
    MessageHandler, Filters, CallbackContext

# Enable logging
# from app import submit, delete, add_poll, add_admin, delete_admin, delete_poll, add_answer
import backend.app
from config import BOT_KEY

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.


def poll(chat_id, question, answers, multiple_choice) -> None:
    """Sends a predefined poll"""

    message = Bot(BOT_KEY).send_poll(
        chat_id[0],
        question,
        answers,
        is_anonymous=False,
        allows_multiple_answers=multiple_choice,
    )
    if multiple_choice == "true":
        multiple_choice = 1
    else:
        multiple_choice = 0
    ans = [0 for a in answers]
    backend.app.add_poll(message.poll.id, question, answers, ans, 0, multiple_choice, 0, [], "")
    real_ID = message.poll.id
    backend.app.add_mapping(real_ID, real_ID)
    if len(chat_id)>1:
        for i in range(1, len(chat_id)):
            message = Bot(BOT_KEY).send_poll(
                chat_id[i],
                question,
                answers,
                is_anonymous=False,
                allows_multiple_answers=multiple_choice,
            )
            backend.app.add_mapping(real_ID, message.poll.id)



def receive_poll_answer(update: Update, context: CallbackContext) -> None:
    """Summarize a users poll vote"""
    answer = update.poll_answer
    print("answer\n")
    print(answer)
    fake_ID = answer.poll_id
    chat_id = answer.user.id
    chosen_answer = answer.option_ids
    backend.app.add_answer(fake_ID, chat_id, chosen_answer, 1)



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
    backend.app.delete(str(user.id))
    update.message.reply_markdown_v2(
        'You are now removed\.\n'
        # reply_markup=ForceReply(selective=True),
    )


def register(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    try:
        backend.app.submit(str(user.id), user.name)
        #add_poll("Is Daniel Balool", ["yes", "no", "obviously"], [0,0,0], 0, 0, 0, [0], "yes" )
        #delete_admin("yaron")
        #delete_poll("1")
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
    updater = Updater(BOT_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))
    #dispatcher.add_handler(CommandHandler('poll', poll))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()
    #poll(5045706840, "How are you?", ["Good", "Really good", "Fantastic", "Great"], False)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
