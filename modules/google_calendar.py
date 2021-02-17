import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

CREDENTIALS_FILE = "not_share/credentials.json"


def get_calendar_service():
    creds = None
    if os.path.exists("not_share/token.pickle"):
        with open("not_share/token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open("not_share/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service


def get_event_list():
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + "Z"  #
    calendar = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = calendar.get("items", [])
    event_list = []
    for event in events:
        event_full = (
            (event["start"].get("dateTime", event["start"].get("date"))).split("T")[0]
            + " "
            + (event["start"].get("dateTime", event["start"].get("date")))
            .split("T")[1]
            .split("+")[0]
            + " "
            + event["summary"]
        )
        event_list.append(event_full)
    return event_list


# def main():
#    service = get_calendar_service()
#    # Call the Calendar API
#    print('Getting list of calendars')
#    calendars_result = service.calendarList().list().execute()
#
#    calendars = calendars_result.get('items', [])
#
#    if not calendars:
#        print('No calendars found.')
#    for calendar in calendars:
#        summary = calendar['summary']
#        id = calendar['id']
#        primary = "Primary" if calendar.get('primary') else ""
#        print("%s\t%s\t%s" % (summary, id, primary))
#
# if __name__ == '__main__':
#    main()
