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
		self.notes = []
		self.on_pic_dict = {}
		self.settings = setting_file_name
		self.id_notes = 0
		self.load()
		
	def addChannel(self,key,value):
		self.channels[key] = value
		print "Channel added"
		
	def addChat(self,key,value):
		self.chats[key] = value
		print "Chat added"
	def addnote(self,notiz,user_id):
		self.notes.append({self.id_notes : {user_id : notiz[1::]}})
		print "node No.%d added" %self.id_notes
		self.id_notes +=1
		
	def save(self):					#Daten in Datei speichern
		f = open(self.settings, 'w')
		pickle.dump(self.__dict__, f)
		f.close()

	def load(self):					#Gespeicherte Daten aus Datei laden
		f = open(self.settings, 'r')
		tmp_dict = pickle.loads(f.read())
		f.close()
		self.__dict__.update(tmp_dict)	
		
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
	command = msg['text'].lower().split()
	print('Chat:', content_type, chat_type, chat_id)
	
	if chat_type == 'group' and chat_id not in sekretaer.channels.values():
       		sekretaer.channels.update({bot.getChat(chat_id)['title'] : chat_id})
        	print "channel added to database"
	if command[0] == 'addnote':
		tmp_user = msg['from']['first_name']
		sekretaer.addnote(command,tmp_user)
		bot.sendMessage(chat_id,"Notiz notiert!")

	if command[0] == 'notes?':
		pass
	
	
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
