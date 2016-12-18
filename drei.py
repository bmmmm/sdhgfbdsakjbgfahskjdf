import sys
import time
import threading
import random
import telepot

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

myChannels = {}
message_with_inline_keyboard = None

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    photo_Wu = 'http://hot97svg.com/wp-content/uploads/2014/10/Wu-Tang-Clan.jpg'

    if content_type != 'text':
        return

    command = msg['text'].lower().split()
    print "Nachricht: %s" %command
    print myChannels.values()

    #print bot.getChat(chat_id)['title']


    if chat_type == 'group' and chat_id not in myChannels.keys():
        myChannels.update({chat_id : bot.getChat(chat_id)['title']})
        print "channel added"



    if len(command)>1 and chat_type=='private':
        '''
        Im privaten Chat, Comando nach " " aufgeteilt
        '''
        if command[0] == 'shout':

            #Area51
            bot.sendMessage(-190416228,' '.join(command[1::] ))
            #VereindFdIfcD
            #bot.sendMessage(-156542408,' '.join(map(str,command[1::] )))

    if 'wu' in command:
        return bot.sendPhoto(chat_id, photo_Wu)

    if 'verein' in command:
        this_msg = 'Verein?! Beschder Verein:\n *%s!*' % bot.getChat(chat_id)['title']
        bot.sendMessage(chat_id, this_msg, 'Markdown')



    if len(command)>1 and chat_type=='group':
        '''
        im Gruppenchat, Comandos nach " " aufgeteilt
        '''
        if command[0] == 'tellme':
            if command[1] == 'groupname':
                this_group = "thisgroup"
                print this_group

        if command[0] == 'a' and command[1] == 'a':
            pass


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)



def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('%s: Computing for: %s' % (threading.current_thread().name, query_string))

        result_type = query_string[-1:].lower()
    if result_type == 'test':
        pass
    else:
        return 1

    answerer.answer(msg, compute)


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)

bot = telepot.Bot('sssss')
answerer = telepot.helper.Answerer(bot)

bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result})
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
