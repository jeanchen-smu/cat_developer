#!/usr/bin/env python
# -*-coding=utf-8 -*-

from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
from services.TelegramService import Telegram
import subprocess
from datetime import datetime, timedelta
from config import config

def get_timelimit(hour):
    now = datetime.now()
    timelimit = now + timedelta(hour)
    return timelimit.strftime(config.date_format)

telegramService = Telegram()

bot_token = '307726211:AAGwbZh2nQ93i3Tf8jUoE9Ag51WCercXe5c'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BUTTON_REPLY, TITLE, CONTENT, QACOIN, TIMELIMIT, SUBMIT, CANCEL, ANSWERREPLY, ANSWER, QUESTIONID, ACCOUNT_VERIFICATION = range(11)

def facts_to_str(user_data):
    facts = list()
    for key, value in user_data.items():
        facts.append('%s - %s' % (key, value))
    return "\n".join(facts).join(['\n', '\n'])

def _process_string(string):
    return string.replace("'", "\'")
'''
def button(bot, update):
    reply_keyboard = [['TITLE', 'CONTENT'],
		      ['QACOIN', 'TIMELIMIT']]
    update.message.reply_text('Please choose another field.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BUTTON_REPLY
'''

def button_reply(bot, update, user_data):
    if update.message.text == 'TITLE':
        update.message.reply_text('What is the title of your post?')
        return TITLE 
    elif update.message.text == 'CONTENT':
        update.message.reply_text('What is your question in detail?')
        return CONTENT
    elif update.message.text == 'QACOIN':
        update.message.reply_text('How many QA Coins you want to put? Send /skip if you dont want to.')
        return QACOIN
    elif update.message.text == 'TIMELIMIT':
        update.message.reply_text('How many hours later would the QA Coins be expired? Send /skip if you dont want to.')
        return TIMELIMIT
    elif update.message.text == 'SUBMIT':
        if 'title' not in user_data:
            update.message.reply_text('Please fill in TITLE.')
            return TITLE
        elif 'content' not in user_data:
            update.message.reply_text('Please fill in CONTENT.')
            return CONTENT
        elif ('qacoin' not in user_data) and ('timelimit' in user_data):
            update.message.reply_text('Please fill in QACOIN. How many QA Coins you want to put?')
            return QACOIN
        elif ('qacoin' in user_data) and ('timelimit' not in user_data):
            update.message.reply_text('Please fill in TIMELIMIT. How many hours later would the QA Coins be expired?')
            return TIMELIMIT
        else:
            if 'qacoin' not in user_data:
                user_data['qacoin'] = 0
            if 'timelimit' not in user_data:
                user_data['timelimit'] = get_timelimit(4)
            user_data['chat_id'] = update.message.chat_id
            try:
                question_id = telegramService.newPost(user_data)
            except Exception as e:
                update.message.reply_text('Fail: your post is not created')
                user_data.clear()
                return ConversationHandler.END
            p = subprocess.Popen(["python telePushMsg.py -i '{}' -q '{}' -t '{}' -c '{}' -w tele".format(
                user_data['chat_id'], question_id, _process_string(user_data['title']), _process_string(user_data['content'])
            )], shell=True)
            update.message.reply_text('Succeed: your post is created')
            user_data.clear()
            return ConversationHandler.END
    elif update.message.text == 'CANCEL':
        update.message.reply_text('Stop posting successfully.')
        user_data.clear()
        return ConversationHandler.END



def newpost(bot, update):
    reply_keyboard = [['TITLE', 'CONTENT'],
		      ['QACOIN', 'TIMELIMIT'],
                      ['SUBMIT', 'CANCEL']]
    print update.message.chat_id
    update.message.reply_text('Start a new post\n\n'
        'Please choose a field to start with.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BUTTON_REPLY

def title(bot, update, user_data):
    user = update.message.from_user
    logger.info("title of %s: %s" % (user.first_name, update.message.text))
    user_data['title']=update.message.text.encode('utf-8')
    reply_keyboard = [['TITLE', 'CONTENT'],
		      ['QACOIN', 'TIMELIMIT'],
                      ['SUBMIT', 'CANCEL']]
    update.message.reply_text('Please choose another field.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BUTTON_REPLY


def content(bot, update, user_data):
    user = update.message.from_user
    logger.info("content of %s: %s" % (user.first_name, update.message.text))
    user_data['content']=update.message.text.encode('utf-8')
    reply_keyboard = [['TITLE', 'CONTENT'],
		      ['QACOIN', 'TIMELIMIT'],
                      ['SUBMIT', 'CANCEL']]
    update.message.reply_text('Please choose another field.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BUTTON_REPLY


def qacoin(bot, update, user_data):
    user = update.message.from_user
    logger.info("qacoin of %s: %s" % (user.first_name, update.message.text))
    user_qacoin = telegramService.get_user_qacoins(update.message.chat_id)
    reply_text = "You do not have enough QA Coins, please fill in QACOIN"
    reply_keyboard = [['TITLE', 'CONTENT'],
                ['QACOIN', 'TIMELIMIT'],
                        ['SUBMIT', 'CANCEL']]
    try:
        if user_qacoin >= int(update.message.text):
            reply_text = "Please choose another field."
        user_data['qacoin']=update.message.text
        update.message.reply_text(reply_text,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    except:
        update.message.reply_text("QA Coins has to be integer, please choose QACOIN.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BUTTON_REPLY

def skip(bot, update):
    reply_keyboard = [['TITLE', 'CONTENT'],
		      ['QACOIN', 'TIMELIMIT'],
                      ['SUBMIT', 'CANCEL']]
    update.message.reply_text('Please choose another field.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BUTTON_REPLY

def timelimit(bot, update, user_data):
    user = update.message.from_user
    logger.info("timelimit of %s: %s" % (user.first_name, update.message.text))
    reply_keyboard = [['TITLE', 'CONTENT'],
		      ['QACOIN', 'TIMELIMIT'],
                      ['SUBMIT', 'CANCEL']]
    try:
        user_data['timelimit']=get_timelimit(float(update.message.text))
        update.message.reply_text('Please choose another field.',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    except:
        update.message.reply_text('Time Limit has to be a number, please choose TIMELIMIT.',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return BUTTON_REPLY

def cancel(bot, update, user_data):
    user = update.message.from_user
    logger.info("User %s canceled the posting process." % user.first_name)
    bot.send_message(chat_id = update.message.chat_id, text = 'Stop posting successfully.')
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def unknown(bot, update):
    bot.send_message(chat_id = update.message.chat_id, 
    text = "Commands:\n New Post: /newpost \nReply to Post: /reply \nAccount Verification: /verify")

def answer_reply(bot, update, user_data):
    if update.message.text == 'QUESTIONID':
        update.message.reply_text('What is the id of the question you are replying to?')
        return QUESTIONID 
    elif update.message.text == 'ANSWER':
        update.message.reply_text('What is your answer to the question?')
        return ANSWER
    elif update.message.text == 'SUBMIT':
        if 'question_id' not in user_data:
            update.message.reply_text('Please fill in QUESTIONID.')
            return QUESTIONID
        elif 'answer' not in user_data:
            update.message.reply_text('Please fill in ANSWER.')
            return ANSWER
        else:
            user_data['chat_id'] = update.message.chat_id
            try:
                telegramService.replyToPost(user_data)
            except Exception as e:
                print e
                update.message.reply_text('Fail: your reply is not created')
                user_data.clear()
                return ConversationHandler.END
            update.message.reply_text('Succeed: your reply is created')
            user_data.clear()
            return ConversationHandler.END
    elif update.message.text == 'CANCEL':
        update.message.reply_text('Stop posting successfully.')
        user_data.clear()
        return ConversationHandler.END

def reply(bot, update):
    reply_keyboard = [['QUESTIONID', 'ANSWER'],
                      ['SUBMIT', 'CANCEL']]
    update.message.reply_text('Start a new reply\n\n'
        'Please click on QUESTIONID to reply.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ANSWERREPLY

def question_id(bot, update, user_data):
    user = update.message.from_user
    logger.info("question_id of %s: %s" % (user.first_name, update.message.text))
    user_data['question_id']=update.message.text
    reply_keyboard = [['QUESTIONID', 'ANSWER'],
                      ['SUBMIT', 'CANCEL']]
    update.message.reply_text('Please click ANSWER to fill in your answer.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ANSWERREPLY

def answer(bot, update, user_data):
    user = update.message.from_user
    logger.info("answer of %s: %s" % (user.first_name, update.message.text))
    user_data['answer']=update.message.text.encode('utf-8')
    reply_keyboard = [['QUESTIONID', 'ANSWER'],
                      ['SUBMIT', 'CANCEL']]
    update.message.reply_text('Please click SUBMIT to submit your answer.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ANSWERREPLY

def account_verify(bot, update, user_data):
    if update.message.text == 'VERIFY':
        user_id = update.effective_user.id
        username = update.effective_user.username
        if telegramService.verify_telgram(username):
            telegramService.upsert_chat_id(user_id, username)
            update.message.reply_text('Succed: your account has been verified.')
            user_data.clear()
            return ConversationHandler.END
        update.message.reply_text('Failed: your account cannot be verified.')
        user_data.clear()
        return ConversationHandler.END
    elif update.message.text == 'CANCEL':
        update.message.reply_text('You have stopped the verification process.')
        user_data.clear()
        return ConversationHandler.END

def verify(bot, update):
    reply_keyboard = [['VERIFY', 'CANCEL']]
    update.message.reply_text('Please click on VERIFY to start the verification process',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ACCOUNT_VERIFICATION




#def main():
    # Create the EventHandler and pass it your bot's token.
updater = Updater(bot_token)
# Get the dispatcher to register handlers
dp = updater.dispatcher
# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conv_handler = ConversationHandler(
entry_points=[CommandHandler('newpost', newpost)],
states={
    BUTTON_REPLY: [RegexHandler('^(TITLE|CONTENT|QACOIN|TIMELIMIT|SUBMIT|CANCEL)$', button_reply, pass_user_data=True), 
                    CommandHandler('newpost', newpost), CommandHandler('reply', reply)],
    TITLE: [MessageHandler(Filters.text, title, pass_user_data=True), CommandHandler('newpost', newpost), CommandHandler('reply', reply)],
    CONTENT: [MessageHandler(Filters.text, content, pass_user_data=True), CommandHandler('newpost', newpost), CommandHandler('reply', reply)],
    QACOIN: [MessageHandler(Filters.text, qacoin, pass_user_data=True),
               CommandHandler('skip', skip), CommandHandler('newpost', newpost), CommandHandler('reply', reply)],
    TIMELIMIT: [MessageHandler(Filters.text, timelimit, pass_user_data=True),
               CommandHandler('skip', skip), CommandHandler('newpost', newpost), CommandHandler('reply', reply)]
},
fallbacks=[CommandHandler('cancel', cancel)]
)
reply_handler = ConversationHandler(
entry_points=[CommandHandler('reply', reply)],
states={
    ANSWERREPLY: [RegexHandler('^(QUESTIONID|ANSWER|SUBMIT|CANCEL)$', answer_reply, pass_user_data=True), 
                    CommandHandler('newpost', newpost), CommandHandler('reply', reply)],
    QUESTIONID: [MessageHandler(Filters.text, question_id, pass_user_data=True), CommandHandler('newpost', newpost), CommandHandler('reply', reply)],
    ANSWER: [MessageHandler(Filters.text, answer, pass_user_data=True), CommandHandler('newpost', newpost), CommandHandler('reply', reply)]
},
fallbacks=[CommandHandler('cancel', cancel)]
)
verify_handler = ConversationHandler(
entry_points=[CommandHandler('verify', verify)],
states={
    ACCOUNT_VERIFICATION: [RegexHandler('^(VERIFY|CANCEL)$', account_verify, pass_user_data=True), 
                    CommandHandler('newpost', newpost), CommandHandler('reply', reply)]
},
fallbacks=[CommandHandler('cancel', cancel)]
)
dp.add_handler(conv_handler)
dp.add_handler(reply_handler)
dp.add_handler(verify_handler)
unknown_handler = MessageHandler(Filters.text, unknown)
dp.add_handler(unknown_handler)
# log all errors
dp.add_error_handler(error)
# Start the Bot
updater.start_polling()
# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()


#if __name__ == '__main__':
#    main()
