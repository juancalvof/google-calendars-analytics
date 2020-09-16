from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import pickle
import datetime
from typing import Dict, Tuple, Sequence


def create_save_credentials():
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file("RESOURCES/client_secret.json", scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))


def retrieve_service():
    credentials = pickle.load(open("RESOURCES/token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    return service


def retrieve_list_calendars():
    # Retrieve calendars
    service = retrieve_service()
    list_calendars = service.calendarList().list().execute()
    return list_calendars


def retrieve_calendar_events_by_id(id_calendar) -> Dict:
    # Retrieve elements of calendar filtering status cancelled
    service = retrieve_service()
    result = service.events().list(calendarId=id_calendar, timeZone="Europe/Madrid").execute()["items"]
    result = [x for x in result if x["status"] != "cancelled"]
    return result


def create_event(calendar_id, start_time_str, summary, duration=1, description=None, location=None):

    # #Option A
    # matches = list(datefinder.find_dates(start_time_str))
    # if len(matches):
    #     start_time = matches[0]
    #     end_time = start_time + datetime.timedelta(hours=duration)

    # #Option B
    # start_time = datetime(2020, 8, 12, 19, 30, 0)
    # end_time = start_time + timedelta(hours=4)
    # timezone = 'Europe/Madrid'

    # Option C
    end_time = start_time_str + datetime.timedelta(hours=duration)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time_str.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/Madrid',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    service = retrieve_service()
    return service.events().insert(calendarId=calendar_id, body=event).execute()
