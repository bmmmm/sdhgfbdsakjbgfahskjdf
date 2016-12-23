import sys
import time
import threading
import random
import telepot
import pickle


from sense_hat import SenseHat
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

class BotManagement(object):
	
	def __init__(self,setting_file_name ):
		self.channels = {}
		self.chats = {}
		self.users = {}
		self.on_pic_dict = {}
		self.settings = setting_file_name
		self.load()
		
	def addChannel(self,key,value):
		self.channels[key] = value
		print "Channel added"
		
	def addChat(self,key,value):
		self.chats[key] = value
		print "Chat added"
		
	def save(self):					#Daten in Datei speichern
		with open(self.settings, 'w') as fp:
			pickle.dump(sekretaer,fp)
	def load(self):					#Gespeicherte Daten aus Datei laden
		with open(self.settings, 'r') as fp:
			loaded =  pickle.loads(fp.read())
		self.channels = loaded.channels
		print loaded.channels
		self.chats = loaded.chats
		self.on_pic_dict = loaded.on_pic_dict
		self.users = loaded.users 
		
		print "settings loaded"
		
	def connectionKey(self):		#Key datei laden
		with open('key.txt', 'r') as fp:
			return fp.readline()
	
		
			

def on_chat_message(msg):
	
	if msg['from']['id'] not in sekretaer.users:
		temp_dict = msg['from'] 
		sekretaer.users[temp_dict.pop('id')] = [temp_dict]
		# TO FIX RICHTIG USERDATABASE ANLEGEN
		print "user added to database"
	
	content_type, chat_type, chat_id = telepot.glance(msg)

	print('Chat:', content_type, chat_type, chat_id)
	
	if chat_type == 'group' and chat_id not in sekretaer.channels.values():
       		sekretaer.channels.update({bot.getChat(chat_id)['title'] : chat_id})
        	print "channel added to database"
	
	
	
	
def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)	
	
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
	
# start init HERE
sense = SenseHat()
sense.clear()
message_with_inline_keyboard = None
settings_2load = "BotStorage.json"
# start until HERE

# Botsettins Config start HERE
sekretaer = BotManagement(settings_2load) # lokalen Bot erzeugen und settings laden	

# Botsettins Config until HERE

bot = telepot.Bot(sekretaer.connectionKey())
answerer = telepot.helper.Answerer(bot)
try:
	bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result})
	print('Listening ...')
	
except:
	e = sys.exc_info()[1]
	print "message loop error:" 
	print e
	
try:
	while 1:
		print sekretaer.channels.keys()
		print sekretaer.users
		time.sleep(10)
		
except KeyboardInterrupt:
		try:
			sekretaer.save()
			print 'last save'
		except:	
			e = sys.exc_info()[1]
			print "last save Error!"
			print e
	
#print sekretaer.connectionKey()
