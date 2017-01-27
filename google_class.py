from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Telebot'

class Google(object):
    """
    Google Schnittstelle
    """
    def __init__(self):
        self.gCal_service = self.setup_service()
        self.created_id = 0
        self.ids = {}
        
        

    def get_credentials(self):
        """Gets valid user credentials from storage.

            If nothing has been stored, or if the stored credentials are invalid,
            the OAuth2 flow is completed to obtain the new credentials.

            Returns:
                Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def show_Events(self, beschreibung):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """    
        #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        today = datetime.date.today()
        monat = today.month
        year = today.year
        first_day_of_month =  datetime.datetime(year,monat,1,0,0)
        fomr_beginning = first_day_of_month.isoformat() + 'Z'
        summe = datetime.time(0,0)
        print('Getting events for %s' %monat)
        eventsResult = self.gCal_service.events().list( 
            calendarId='primary',q = beschreibung, timeMin=fomr_beginning, singleEvents=True, #, maxResults=10
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        print ("Anzahl: %s" %len(events))
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end  = event['end'].get('dateTime', event['end'].get('date'))
            #print(start, event['summary'])
            count = start.rfind("+")    # Timezone wegschneiden
            form_end = datetime.datetime.strptime(end[:count],"%Y-%m-%dT%H:%M:%S") 
            form_start =  datetime.datetime.strptime(start[:count],"%Y-%m-%dT%H:%M:%S")
            dauer = form_end - form_start
            #summe = summe + datetime.timedelta (dauer)
            print("%s Dauer : %s : %s" % (beschreibung, dauer,start[:count-3])) #Sekunden wegschneiden
        #print (summe)

    def make_Event(self,beschreibung):
        #beschreibung = "telebot2"
        now = datetime.datetime.utcnow()
        future_now = now + datetime.timedelta(hours=5)  # 5 Stunden addieren
        now = now.isoformat() + 'Z' # 'Z' indicates UTC time
        future_now =future_now.isoformat() + 'Z' 
        event = {
          'summary': beschreibung,
          'location': 'internetz',
          'description': 'good to know',
          'end': {
            'dateTime': future_now,
            'timeZone': 'Europe/Berlin',
          },
          'start': {
            'dateTime': now,
            'timeZone': 'Europe/Berlin',
          },
          'reminders': {
            'useDefault': True,
          },}           
        event = self.gCal_service.events().insert(calendarId='primary', body=event).execute()
        self.created_id +=1
        self.ids.update({self.created_id : event['id']})            # HIIIER ABSPEICHERN!!!
        print ('Event created: %s' % (self.ids))
        return self.ids
        
    def update_Event(self,this_id):
        #this_id = 'br39v72ch8iq84ehk85grbk0ko' #MUSS BEKANNT SEIN !!!
        
        antwort_event = self.gCal_service.events().get(calendarId='primary', eventId=this_id).execute()
        #print (antwort_event)
        now2 = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        antwort_event['end']['dateTime'] = now2
        updated_event = self.gCal_service.events().update(calendarId='primary', eventId=antwort_event['id'], body=antwort_event).execute()
        print ("updated time to : %s" % updated_event['updated'])

    def setup_service(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service        

    
