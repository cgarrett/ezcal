"""EZCal - A Pythonic interface to the Google Calendar API."""

# Original concept by Al Sweigart al@inventwithpython.com (based on his EZGmail module)
# Note: Unless you know what you're doing, also use the default 'me' value for userId parameters in this module.

__version__ = "2020.11.02"

import base64
import os
import datetime
import re
import copy
import warnings

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SERVICE_GCAL = None
EMAIL_ADDRESS = False  # False if not logged in, otherwise the string of the email address of the logged in user.
LOGGED_IN = False # False if not logged in, otherwise True

class EZCalException(Exception):
    """ Base class for EZCal Exceptions """
    pass

class EZCalCalendarList():
    """ This class represents a collection of calendars in the user's calendar list. """
    def __init__(self, calendarListObj):
        self.calendarListObj = copy.deepcopy(calendarListObj)
        self.id = calendarListObj["id"]
        self.etag = calendarListObj["etag"]
        self.summary = calendarListObj["summary"]
        self.description = calendarListObj["description"]
        self.location = calendarListObj["location"]
        self.timeZone = calendarListObj["timeZone"]
        self.hidden = calendarListObj["hidden"]
        self.selected = calendarListObj["selected"]
        self.accessRole = calendarListObj["accesRole"]
        self._defaultReminders = None
        self._notificationSettings = None
        self.primary = calendarListObj["primary"]
        self.deleted = calendarListObj["deleted"]



def init(userId="me", tokenFile="token.json", credentialsFile="credentials.json", _raiseException=True):
    global SERVICE_GCAL, EMAIL_ADDRESS, LOGGED_IN
    EMAIL_ADDRESS = False
    LOGGED_IN = False

    try:
        if not os.path.exists(credentialsFile):
            raise EZCalException(
                f'Can\'t find credentials file at {os.path.abspath(credentialsFile)}. You can download this file from https://developers.google.com/calendar/quickstart/python and clicking "Enable the Google Calendar API". Rename the downloaded file to credentials.json.'
            )

        store = file.Storage(tokenFile)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentialsFile, SCOPES)
            creds = tools.run_flow(flow, store)
        SERVICE_GCAL = build("calendar", "v3", http=creds.authorize(Http()))
        EMAIL_ADDRESS = SERVICE_GCAL.users().getProfile(userId=userId).execute()["emailAddress"]
        LOGGED_IN = bool(EMAIL_ADDRESS)

        return EMAIL_ADDRESS
    except:
        if _raiseException:
            raise
        else:
            return False