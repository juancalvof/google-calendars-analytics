from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import streamlit as st
import pickle
import datetime
from typing import Dict, Tuple, Sequence

import datefinder

JSON_CLIENT_SECRET = "RESOURCES/client_secret_gca_testing_user.json"
TOKEN = "RESOURCES/token_gca_testing_user.pkl"


def create_save_credentials():
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file(JSON_CLIENT_SECRET, scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open(TOKEN, "wb"))


# TODO Test cache_discovery in True. Error message. Performance. MemoryCache()
def retrieve_service():
    credentials = pickle.load(open(TOKEN, "rb"))
    service = build("calendar", "v3", credentials=credentials, cache_discovery=False)
    return service


def retrieve_list_calendars():
    # Retrieve calendars
    service = retrieve_service()
    list_calendars = service.calendarList().list().execute()
    return list_calendars


def retrieve_calendar_events_by_id(id_calendar) -> Dict:
    # Retrieve elements of calendar filtering status cancelled
    service = retrieve_service()
    page_token = None
    result = []
    while True:
        events = service.events().list(calendarId=id_calendar, pageToken=page_token, singleEvents=True,
                                       orderBy="startTime").execute()
        result += events["items"]
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    result = [x for x in result if x["status"] != "cancelled"]
    return result


def delete_events(id_calendar, events):
    service = retrieve_service()
    for event in events:
        service.events().delete(calendarId=id_calendar, eventId=event["id"]).execute()


def create_event(type_time, calendar_id, start_time_str, summary, duration=1, description=None, location=None,
                 recurrence=None):
    start_time = None

    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]

    type_format = "%Y-%m-%dT%H:%M:%S"
    if type_time == "date":
        type_format = "%Y-%m-%d"

    start_time_str_dict = start_time.strftime(type_format)
    end_time = start_time + datetime.timedelta(hours=duration)
    end_time_str_dict = end_time.strftime(type_format)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            type_time: start_time_str_dict,
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            type_time: end_time_str_dict,
            'timeZone': 'Europe/Madrid',
        },
        'recurrence': [
            'RRULE:FREQ=' + recurrence
        ],
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
