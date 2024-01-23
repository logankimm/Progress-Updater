import requests
import json
import os
import sys
import pathlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.file import Storage
from googleapiclient.errors import HttpError

class Google_APIs:
    credentials = None
    TOKEN_SCOPES = None
    def __init__(self, scopes: list, credentials_path = "credentials\\client-secret.json", token_path = "credentials\\tokens.json"):
        self.TOKEN_SCOPES = scopes
        curr_dir = os.path.dirname(os.path.abspath(__file__))

        # check if credentials_path is default
        if (credentials_path == "credentials\\client-secret.json"):
            credentials_path = os.path.join(os.path.split(curr_dir)[0], credentials_path)

        if (token_path ==  "credentials\\tokens.json"):
            token_path = os.path.join(os.path.split(curr_dir)[0], token_path)

        if os.path.exists(token_path):
            self.credentials = Credentials.from_authorized_user_file(token_path, self.TOKEN_SCOPES)

        # if not credentials or they're not valid
        if not self.credentials or not self.credentials.valid:
            # if there are credentials or they're invalid now
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.TOKEN_SCOPES)
                self.credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(self.credentials.to_json())


SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]
# spread_id = "1peDrk9b9fnRcMSSk_GMp1F7C8UR6SCXrB0DbElPu9Lw"

asdf = Google_APIs(SCOPES)

# print(os.path.dirname(os.path.abspath(__file__)) + "/token.json")
# print(os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.json"))

# if os.path.exists(filepath):
#     print (filepath + ' exists')
# else: 
#     print (filepath + ' does not exist')

# print(os.path.join(os.getcwd(), "token.json"))
# print(os.path.exists("google_apis.py".strip()))