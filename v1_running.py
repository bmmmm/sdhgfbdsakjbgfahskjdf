import sys
import time
import threading
import random
import telepot
import pickle
import datetime

#from sense_hat import SenseHat

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

	def addnote(self,notiz,user_name):
		self.notes.append({self.id_notes : {user_name : notiz[1::]}})
		print "node No.%d added" %self.id_notes
		self.id_notes +=1
	
	def show_notes(self,chat_id):
		try:
			for note_number in range(len(self.notes)):
				tmp_note_numer = self.notes[note_number].keys()[0]
				tmp_note_user = self.notes[note_number].values()[0].keys()[0]
				tmp_note_msg = self.notes[note_number].values()[0].values()[0]
				mystr = ""
				for i in range(len(tmp_note_msg)):
					mystr +="%s " % tmp_note_msg[i]
				sending_msg = "nodeID : {!s} - user: {!s}  - Notziz: {!s}".format(tmp_note_numer,tmp_note_user,mystr.encode('utf-8'))
				bot.sendMessage(chat_id,sending_msg)

		except:
			e = sys.exc_info()[1]
			print "showing notes error:" 
			print e

	def del_note(self,chat_id,note_nr):
		try:
			del self.notes[note_nr]
			sending_msg= "Deleted note ID #%d" %note_nr
			print sending_msg
			bot.sendMessage(chat_id,sending_msg)

		except:
			sending_msg = "No note with ID #%d"  %note_nr
			print sending_msg
			bot.sendMessage(chat_id,sending_msg)		

	def save(self):					#Daten in Datei speichern
		f = open(self.settings, 'w')
		pickle.dump(self.__dict__, f)
		f.close()

	def load(self):					#Gespeicherte Daten aus Datei laden
		try:
			f = open(self.settings, 'r')
			tmp_dict = pickle.loads(f.read())
			f.close()
			self.__dict__.update(tmp_dict)	
			print "settings loaded"
		except:
			print "loading error"

	def connectionKey(self):		#Key datei laden
		with open('key.txt', 'r') as fp:
			return fp.readline()
	
		
			

def on_chat_message(msg):
	global time_started
	
	if msg['from']['id'] not in sekretaer.users:
		temp_dict = msg['from'] 
		sekretaer.users[temp_dict.pop('id')] = [temp_dict]
		# TO FIX RICHTIG USERDATABASE ANLEGEN
		print "user added to database"
	
	photo_Wu = 'http://hot97svg.com/wp-content/uploads/2014/10/Wu-Tang-Clan.jpg'

	content_type, chat_type, chat_id = telepot.glance(msg)
	command = msg['text'].lower().split()
	#print('Chat:', content_type, chat_type, chat_id)
	
	if chat_type == 'group' and chat_id not in sekretaer.channels.values():
       		sekretaer.channels.update({bot.getChat(chat_id)['title'] : chat_id})
        	print "channel added to database"

	if 'func' in command:
		sending_msg=('Ich kann: addnote Notiz; notes?; delnote Nr; onair; wu; verein; ')
		bot.sendMessage(chat_id,sending_msg)
	
	if command[0] == 'addnote':
		tmp_user = msg['from']['first_name']
		sekretaer.addnote(command,tmp_user)
		bot.sendMessage(chat_id,"Notiz notiert!")

	if command[0] == 'notes?':
		sekretaer.show_notes(chat_id)
	
	if command[0] == 'delnote':
		if len(command) == 2:
			sekretaer.del_note(chat_id,int(command[1]))
		else:
			bot.sendMessage(chat_id,"zu viele Argumente")

	if 'onair' in command:
		sending_msg = 'effektiv bin ich seit %s da.' % time_started
		bot.sendMessage(chat_id,sending_msg)

	if 'wu' in command:
		return bot.sendPhoto(chat_id, photo_Wu)

	if 'verein' in command:
		this_msg = 'Verein?! Beschder Verein:\n *%s!*' % bot.getChat(chat_id)['title']
		bot.sendMessage(chat_id, this_msg, 'Markdown')
		#'Markdown' fuer ** bold schreiben / Formatierung
	
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
#sense = SenseHat()
#sense.clear()
time_started = datetime.datetime.now()
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
	print "-- message loop error:" 
	print e
	
try:
	safe_count = 0
	
	while 1:
		print safe_count
		if safe_count == 6:	# nach einer Minute speichern
			try:
				sekretaer.save()
				print '++ auto save done'
				safe_count =0
			except:	
				e = sys.exc_info()[1]
				print "-- auto save Error!"
				print e
				safe_count =0
		print "channels:"	
		print sekretaer.channels.keys()
		print "users:"
		print sekretaer.users
		print "notes:"
		print sekretaer.notes
		safe_count +=1
		time.sleep(10)
		
		
except KeyboardInterrupt:
		try:
			sekretaer.save()
			print '++ last save'
		except:	
			e = sys.exc_info()[1]
			print "-- last save Error!"
			print e
else:	#letzte Nachricht an mich senden
	bot.sendMessage(296276669, "\n$$$$$$$$$$$$$$$$$$$ \nmeine letzten Worte")
	bot.sendMessage(296276669,sys.exc_info()[1])	
#print sekretaer.connectionKey()
