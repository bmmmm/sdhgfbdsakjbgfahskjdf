import sys
from time import strftime, mktime, strptime, gmtime, time, sleep
import threading
import telepot, pickle, datetime
import pprint
import google_class, md5, urllib2

# from sense_hat import SenseHat
onpi = True
if onpi is True:
    from sense_hat import SenseHat

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent


class BotManagement(object):
    """

    Botklasse
    """

    def __init__(self, setting_file_name):
        self.channels = {}
        self.chats = {}
        self.users = {}
	self.hashLib = {}
        self.notes = {}
        self.on_pic_dict = {}
        self.settings = setting_file_name
        self.id_notes = 0
        self.gcal_IDs = 0
        self.gcal_IDs_dict = {}
        self.invite_dict = {}
        self.event_Timer_dict = {}
        self.today_Event_dic_count = 0
        self.load()

    def addChannel(self, key, value):
        self.channels[key] = value
        print "-------------------------------------------- Channel added"

    def addChat(self, key, value):
        self.chats[key] = value
        print "------------------------------------------------ Chat added"

    def usr_invite(self, user_id, user_msg):

        if not self.invite_dict.has_key(user_id):
            print "{} hat das Codeword gesagt!".format(user_id)
            sending_msg = "tippe start_raetsel um dein Einlassprozess zu beginnen"
            bot.sendMessage(user_id, sending_msg)
            self.invite_dict[user_id] = 1

        else:
            tmp_count = self.invite_dict[user_id]
            # print user_msg
            self.invite_dict[user_id] = tmp_count
            if self.invite_dict[user_id] == 1 and user_msg[0] == "start_raetsel":
                print "user is in stage 1 . Morsecode senden"
                morse_file = open('morsecode.wav', 'r')
                bot.sendMessage(user_id, 'let it got!')
                bot.sendDocument(user_id, morse_file)
                self.invite_dict[user_id] = 2
                morse_file.close()
            if self.invite_dict[user_id] == 2 and user_msg[0] == "bird":
                bot.sendMessage(user_id, '872657 3.1415')
                print "user is in stage 2"
                self.invite_dict[user_id] = 3

            if len(user_msg) == 2:
                if self.invite_dict[user_id] == 3 and user_msg[0] == "raspberry" and user_msg[1] == "pi":
                    stage3_pic = 'https://chrissto.blob.core.windows.net/tets/stegano.png'
                    sending_msg = "Das letzte Raetsel...(benutze URL)"
                    bot.sendMessage(user_id, sending_msg)
                    bot.sendMessage(user_id, stage3_pic)

    def calc_Events(self, user_id, onoff, beschreibung):
        t_format = "%Y-%m-%d %H:%M:%S"
        if user_id not in self.event_Timer_dict:
            # print "go"
            # print onff,beschreibung
            if onoff == "on":
                """
                first run, if user is not in event_Timer_dict -> INIT
                """
                day_started = strftime(t_format)
                today_Event_dict = dict(Beschreibung=str(beschreibung))
                # today_Event_dict.update({"Beschreibung" : str(beschreibung)})
                today_Event_dict.update({"Beginn": str(day_started)})
                today_Event_dict.update({"Ende": "... running"})
                self.event_Timer_dict[user_id] = {self.today_Event_dic_count: today_Event_dict}
                send_msg = "Timer #{} started".format(int(self.today_Event_dic_count))
                bot.sendMessage(user_id, send_msg)
                self.today_Event_dic_count += 1
        else:
            if onoff == "on":
                day_started = strftime(t_format)
                today_Event_dict = dict(Beschreibung=str(beschreibung))
                today_Event_dict.update({"Beginn": str(day_started)})
                today_Event_dict.update({"Ende": "... running"})
                self.event_Timer_dict[user_id].update(
                    {self.today_Event_dic_count: today_Event_dict})
                send_msg = "Timer #{} started".format(int(self.today_Event_dic_count))
                bot.sendMessage(user_id, send_msg)
                self.today_Event_dic_count += 1

            elif onoff == "off":
                try:
                    if int(beschreibung):
                        user_data_Event_id = int(beschreibung)
                        day_ended = strftime(t_format)
                        # last_user_Event = max(self.event_Timer_dict[user_id].values())
                        try:
                            if self.event_Timer_dict[user_id][user_data_Event_id]['Ende'] == '... running':
                                # if beschreibung in self.event_Timer_dict[user_id][user_data_Event_id]['Beschreibung']:
                                self.event_Timer_dict[user_id][user_data_Event_id]['Ende'] = day_ended
                                tmp_start = self.event_Timer_dict[user_id][user_data_Event_id]['Beginn']
                                tmp_ende = self.event_Timer_dict[user_id][user_data_Event_id]['Ende']
                                format_start = mktime(strptime(tmp_start, t_format))
                                format_ende = mktime(strptime(tmp_ende, t_format))
                                tdiff = format_ende - format_start
                                format_tdiff = strftime("%H:%M:%S", gmtime(tdiff))
                                self.event_Timer_dict[user_id][user_data_Event_id].update({"Dauer": format_tdiff})
                                bot.sendMessage(user_id, "Timer stopped")
                        except:
                            print "Error in timer off"
                            bot.sendMessage(user_id, "ERROR! no running")
                            print sys.exc_info()
                except:
                    bot.sendMessage(user_id, "ERROR! wrong timer Event Id to sop")

    def check_Events_running(self, user_id):
        total_string = ""
        events_running = False
        try:
            events_keys = self.event_Timer_dict[user_id].keys()
            for i in events_keys:
                event_values_list = self.event_Timer_dict[user_id][i].values()
                # print event_values_list
                for event_value in event_values_list:
                    if event_value == "... running":
                        try:
                            print "this Event is running"
                            events_running = True
                            tmp_dict = self.event_Timer_dict[user_id][i]
                            timer_number = i
                            timer_started = tmp_dict['Beginn']
                            timer_bez = tmp_dict['Beschreibung']
                            akt_msg = "Timer #{} running...\nBeginn:{}\nBeschreibung: {}\n".format(str(timer_number),
                                                                                                   timer_started,
                                                                                                   timer_bez.encode(
                                                                                                       'utf-8'))
                            total_string += akt_msg
                        except:
                            print "timer timers? 1 "
                            print sys.exc_info()
            if events_running == False:
                bot.sendMessage(user_id, "no events running")
            tmp_user_Events = self.event_Timer_dict[user_id].keys()
            for event_Id in tmp_user_Events:
                tmp_dict = self.event_Timer_dict[user_id][event_Id]
                timer_number = event_Id
                if len(tmp_dict.keys()) == 4:
                    try:
                        timer_duration = tmp_dict['Dauer']
                        timer_started = tmp_dict['Beginn']
                        timer_bez = tmp_dict['Beschreibung']
                        akt_msg = "Timer #{}\nBeginn: {}\nDauer:{}\nBeschreibung: {}\n".format(str(timer_number),
                                                                                               timer_started,
                                                                                               timer_duration,
                                                                                               timer_bez.encode(
                                                                                                   'utf-8'))
                        total_string += akt_msg
                    except:
                        print sys.exc_info()
                        print "timer timers? 2 "
        except:
            print sys.exc_info()
            print "timer timers? 0 "
        # print total_string
        bot.sendMessage(user_id, total_string)

    def del_user_Event(self, user_id, event_id):
        try:
            del self.event_Timer_dict[user_id][event_id]
            bot.sendMessage(user_id, "Timer Event deleted!")
        except:
            bot.sendMessage(user_id, "ERROR! wrong Event Id!")

    def usr_db(self, chat_id):

        for user_id, value_list in self.users.iteritems():
            user_keys = value_list[0].keys()
            user_values = value_list[0].values()
            # print "{!s}".format(str(user_keys))
            keys_str = ""
            for i in range(len(user_keys)):
                keys_str += "%s | " % user_keys[i]
            values_str = ""
            for i in range(len(user_keys)):
                values_str += "%s | " % user_values[i]
            sending_msg = "userid: {}\n{}\n{}".format(str(user_id), keys_str.encode('utf-8'),
                                                      values_str.encode('utf-8'))
            bot.sendMessage(chat_id, sending_msg)

    def usr_add_prop(self, chat_id, user_id, adding_key, adding_value):
        try:
            self.users[user_id][0].update({adding_key: adding_value})
            sending_msg = "success! added information for user_id #{!s}.".format(user_id)
            bot.sendMessage(chat_id, sending_msg)

        except Exception as e:
            print "------------------------------------------------ BOT send adding user level error"
            print "wrong value {}".format(e)

    def usr_del_prop(self, chat_id, user_id, del_key):
        print chat_id, user_id, del_key
        try:
            del self.users[user_id][0][del_key]
            bot.sendMessage(chat_id, "SUCCESS! del_prop")
        except:
            e = sys.exc_info()
            bot.sendMessage(chat_id, "ERROR! del_prop")
            bot.sendMessage(chat_id, str(e))

    def resetnotes(self):
        self.notes = {}
        self.id_notes = 0

    def addnote(self, notiz, user_name):
        self.notes.update({self.id_notes: {user_name: notiz[1::]}})
        print "------------------------------------------------ Note #%d added" % self.id_notes
        self.id_notes += 1

    def show_notes(self, chat_id):
        try:
            sending_msg = ''
            for notenumber, second_dict in sekretaer.notes.iteritems():
                tmp_note_user = second_dict.keys()[0]
                notat = ''
                for val in second_dict.itervalues():
                    for i in xrange(len(val)):
                        notat += "%s " % val[i]
                sending_msg += 'NotizID ' + str(
                    notenumber) + ' notiert von: ' + tmp_note_user + ' - Notat: ' + notat + '\n'
            bot.sendMessage(chat_id, sending_msg)

        except:
            e = sys.exc_info()[1]
            print "------------------------------------------------ showing notes error:"
            print e

    def del_note(self, chat_id, note_nr):
        try:
            del self.notes[note_nr]
            sending_msg = "NotizID %d geloescht." % note_nr
            print sending_msg
            bot.sendMessage(chat_id, sending_msg)

        except:
            sending_msg = "No note with ID #%d" % note_nr
            print sending_msg
            bot.sendMessage(chat_id, sending_msg)
            print sys.exc_info()[0]

    def checkurl(self, urls):
        try:
            site_code = urllib2.urlopen(urls).getcode()
	    if site_code == 200:
                print "Valid URL"
                return True
            else:
                print "ERROR with URL Server"
                return False

        except urllib2.URLError:
            print "ERROR! wrong URL"
            return False

    def save(self):  # Daten in Datei speichern
        f = open(self.settings, 'w')
        pickle.dump(self.__dict__, f)
        f.close()

    def load(self):  # Gespeicherte Daten aus Datei laden
        try:
            f = open(self.settings, 'r')
            tmp_dict = pickle.loads(f.read())
            f.close()
            self.__dict__.update(tmp_dict)
            print "------------------------------------------------ settings loaded"
        except:
            print "------------------------------------------------ loading error"

    def connectionKey(self):  # Key datei laden
        with open('key.txt', 'r') as fp:
            return fp.readline()


def on_chat_message(msg):
    global time_started
    global onpi

    if msg['from']['id'] not in sekretaer.users:
        temp_dict = msg['from']
        sekretaer.users[temp_dict.pop('id')] = [temp_dict]
        # TO FIX RICHTIG USERDATABASE ANLEGEN
        print "------------------------------------------------ user added to database"

    photo_Wu = 'http://hot97svg.com/wp-content/uploads/2014/10/Wu-Tang-Clan.jpg'
    git_rep_link = 'https://github.com/bmmmm/sdhgfbdsakjbgfahskjdf.git'

    content_type, chat_type, chat_id = telepot.glance(msg)

    if chat_id == 296276669:  # id bm
        command = msg['text'].split()

        if len(command) <= 4:
            if command[0] == 'GC':  # google calendar
                mygoogle = google_class.Google()
                if command[1] == 's':  # s for search
                    hours_minutes_string = mygoogle.show_Events(command[2])
                    stunden = hours_minutes_string[0][0]
                    minuten = hours_minutes_string[0][1]
                    if len(command) == 4 and command[3] == 'all':
                        auflistung = hours_minutes_string[1]
                        send_msg2 = '{}'.format(auflistung)
                        bot.sendMessage(chat_id, send_msg2)
                    sending_msg = '[HH:MM] - {}:{}'.format(stunden, minuten)
                    bot.sendMessage(chat_id, sending_msg)
                    print "------------------------------------------------ Event found and calculated"

                if command[1] == 'a':  # a for add
                    tmpdict = mygoogle.make_Event(command[2])
                    sekretaer.gcal_IDs += 1
                    sending_msg = "Event created with id #{}".format(sekretaer.gcal_IDs)
                    bot.sendMessage(chat_id, sending_msg)
                    sekretaer.gcal_IDs_dict = {sekretaer.gcal_IDs: tmpdict.values()[0]}
                    # print sekretaer.gcal_IDs_dict
                    print '------------------------------------------------ EVENT CREATED --------'
                if command[1] == 'u':  # u for update
                    try:
                        dict_key = command[2]
                        tmp_Event_Id = sekretaer.gcal_IDs_dict[int(dict_key)]
                        mygoogle.update_Event(tmp_Event_Id)
                        bot.sendMessage(chat_id, 'Event updated!')
                    except:
                        print "------------------------------------------------ Error in Gcon u!!!"
                        bot.sendMessage(chat_id, 'Event ID not found')
                del mygoogle
        else:
            bot.sendMessage(chat_id, 'zu viele Argumente')

    # HIER WERDEN NACHRICHTEN INFOS ANGEZEIGT:
    print('Chat:', content_type, chat_type, chat_id)
    command = msg['text'].split()
    print ('Command', command)

    if chat_type == 'group' and chat_id not in sekretaer.channels.values():
        sekretaer.channels.update({bot.getChat(chat_id)['title']: chat_id})
        print "------------------------------------------------ channel added to database"

    if 'funk!' in command:
        sending_msg = ("Ich kann:"
                       "\nnotizen?; usrs?; timer?"
                       "\nonair; wu; verein"
                       "\ngit? aup?; dup?"
                       "\nhash?")
        bot.sendMessage(chat_id, sending_msg)

    if onpi is True and chat_id == -156542408:
        print "rot"
        sense.clear(255, 0, 0)  # rot
        sleep(1)
        sense.clear()
        print "sensehat cleared"

    if command[0] == "usrs?":
        sekretaer.usr_db(chat_id)
    if command[0] == "timer?":
        sending_msg = ("[t on Beschreibung] = starte Timer mit Beschreibung"
                       "\n[t off TimerID] = Timer mit ID beenden"
                       "\n[t del TimerID] = Timer mit ID loeschen"
                       "\n[t timers?] = alle Timer anzeigen")

        bot.sendMessage(chat_id, sending_msg)
    if command[0] == 'notizen?':
        sending_msg = ("[addnote Notat] = Notat/Notiz hinzufuegen"
                       "\n[delnote NotizID] = NotizID loeschen"
                       "\n[notes?] = alle eigenen/Channel  Notizen auflisten")
        bot.sendMessage(chat_id, sending_msg)
    if command[0] == "aup?":
        bot.sendMessage(chat_id, "[aup USERID KEY VALUE] => add user property")
    if command[0] == "hash?":
        sending_msg = ("!!! Funktion NUR im privaten Chat moeglich !!!"
                       "\nIch kann folgende  hashes:"
                       "\nMD5,SHA1, SHA256, SHA384, SHA512"
                       "\n[hash HASHTYPE URL/file] = HASHTYPE wird auf URL/file angewendet")
        bot.sendMessage(chat_id, sending_msg)
    if len(command) == 4:
        if command[0] == "aup":
            sekretaer.usr_add_prop(chat_id, int(command[1]), command[2], command[3])

    if command[0] == "dup?":
        bot.sendMessage(chat_id, "[dup USERID KEY] => delete user property")

    if len(command) == 3:
        if command[0] == "dup":
            sekretaer.usr_del_prop(chat_id, int(command[1]), command[2])

    if command[0] == 'addnote':
        tmp_user = msg['from']['first_name']
        sekretaer.addnote(command, tmp_user)
        bot.sendMessage(chat_id, "Notiz notiert!")

    if command[0] == 'notes?':
        sekretaer.show_notes(chat_id)

    if command[0] == 'rrresetnotes':
        sekretaer.resetnotes()
    if command[0] == 't':
        if len(command) > 2:
            if command[1] == 'on':
                sekretaer.calc_Events(chat_id, command[1], command[2::])
            if command[1] == 'off':
                sekretaer.calc_Events(chat_id, command[1], command[2])
            if command[1] == 'del':
                try:
                    sekretaer.del_user_Event(chat_id, int(command[2]))
                except:
                    print "error in del user event"

        if len(command) == 2 and command[1] == 'timers?':
            try:
                sekretaer.check_Events_running(chat_id)
            except:
                bot.sendMessage(chat_id, 'you have no timers')
                print "error in timer timers?"
    if command[0] == 'delnote':
        if len(command) == 2:
            sekretaer.del_note(chat_id, int(command[1]))
        else:
            bot.sendMessage(chat_id, "zu viele Argumente")

    if 'onair' in command:
        sending_msg = 'effektiv bin ich seit %s da.' % time_started
        bot.sendMessage(chat_id, sending_msg)

    if 'wu' in command:
        return bot.sendPhoto(chat_id, photo_Wu)

    if command[0] == 'git?':
        this_msg = 'GitHub repositry:\n%s' % git_rep_link
        bot.sendMessage(chat_id, this_msg, 'Markdown')

    if 'verein' in command:
        this_msg = 'Verein?! Beschder Verein:\n *%s!*' % bot.getChat(chat_id)['title']
        bot.sendMessage(chat_id, this_msg, 'Markdown')
    # 'Markdown' fuer ** bold schreiben / Formatierung
    if chat_type == 'private' and command[0] == 'invite':
        user_id = msg['from']['id']
        user_msg = command[0]
        sekretaer.usr_invite(user_id, user_msg)
    if chat_type == 'private' and command[0] == 'hash':
        if len(command) == 3:  # MD5,SHA1, SHA256, SHA384, SHA512"
	    tmp_cmd = command
            myHash = md5.HASH()
            if tmp_cmd[1].lower() == 'md5':
                myHash.hash_flag = 0
            elif tmp_cmd[1].lower() == 'sha1':
                myHash.hash_flag = 1
            elif tmp_cmd[1].lower() == 'sha256':
                myHash.hash_flag = 2
            elif tmp_cmd[1].lower() == 'sha384':
                myHash.hash_flag = 3
            elif tmp_cmd[1].lower() == 'sha512':
                myHash.hash_flag = 4
            else:
                bot.sendMessage(chat_id, "ERROR wrong hash_flag!")
                print "ERROR wrong hash_flag!"
                return
            if sekretaer.checkurl(command[2]):
		
		# sekretaer.hashLib.update({chat_id: {datetime.datetime.utcnow().isoformat()[:-7]: command[2]}})		
		hashed = myHash.hashFromURL(command[2])
                sending_msg = ("ich habe folgenden hash gefunden"
                               "\nhashtype: {}"
                               "\nhashed file: {}"
                               "\nhash: {}").format(command[1], myHash.downloaded_file, hashed)
               	print command[1], myHash.downloaded_file, hashed
                bot.sendMessage(chat_id, sending_msg)
            else:
                bot.sendMessage(chat_id, "ERROR with URL!")
                print "ERROR! with URL in HASH"
	    del(myHash)
    if chat_type == 'private' and msg['from']['id'] in sekretaer.invite_dict:
        user_id = msg['from']['id']
        user_msg = command[0:2]
        sekretaer.usr_invite(user_id, user_msg)

    if chat_type == 'private' and command[0] == 'sesam' and command[1] == 'oeffne' and command[2] == 'dich':
        user_id = msg['from']['id']
        print " \n------------------------------------------------ !!!! invite user"
        this_msg = 'https://t.me/joinchat/AAAAAAlUpcizR4bfaFnAeA'
        bot.sendMessage(user_id, this_msg, 'Markdown')


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
if onpi == True:
    sense = SenseHat()
    sense.clear()
time_started = datetime.datetime.now()
message_with_inline_keyboard = None
settings_2load = "BotStorage.json"
# start until HERE

# Botsettins Config start HERE
sekretaer = BotManagement(settings_2load)  # lokalen Bot erzeugen und settings laden

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
    print "-------------------------------------------------- message loop error:"
    print e

try:
    safe_count = 0
    while 1:
        print '------------------------------------------------ SAVE COUNT {} ------------------------------------------------'.format(
            safe_count)
        if safe_count == 20:  # nach einer Minute speichern
            try:
                sekretaer.save()
                print '------------------------------------------------ ++ auto save done'
                safe_count = 0
            except:
                e = sys.exc_info()[1]
                print "------------------------------------------------ -- auto save Error!"
                print e
                safe_count = 0
        print "channels: DISABLED"
        # print pprint.pprint(sekretaer.channels.keys())
        print "users: DISABLED"
        # print pprint.pprint(sekretaer.users)
        print "notes: DISABLED"
        # print pprint.pprint(sekretaer.notes)
        # print "user timers:"
        # print pprint.pprint(sekretaer.event_Timer_dict)
        print "invite dict: DISABLED"
        # print sekretaer.invite_dict
        
	safe_count += 1
        sleep(3)

except:
    try:
        print '++ last save'
        sekretaer.save()
        bot.sendMessage(-190416228, "BOT BEENDET")
        bot.sendMessage(-190416228, str(sys.exc_info()))
    except:
        e = str(sys.exc_info()[1])
        print "-- last save Error!"
        print e
        bot.sendMessage(-190416228, "FEHLER bei BOT BEENDEN")
        bot.sendMessage(-190416228, e)
