import requests
import json
import os
import sys
import pathlib
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.file import Storage
from googleapiclient.errors import HttpError

class Google_APIs:
    credentials = None
    TOKEN_SCOPES = None
    def __init__(self, scopes: list, credentials_path = "credentials.json", token_path = "tokens.json"):
        self.TOKEN_SCOPES = scopes
        curr_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        print(curr_dir)

        # check if credentials_path is default
        if (credentials_path == "credentials.json"):
            credentials_path = os.path.join(curr_dir, credentials_path)

        if (token_path == "tokens.json"):
            token_path = os.path.join(curr_dir, token_path)

        if os.path.exists(token_path):
            # Check if token is expired - delete if it is
            expiration_date = None
            current_time = datetime.now() + timedelta(minutes=5)

            # Read expiration date value
            with open(token_path, "r") as json_file:
                token = json.load(json_file)

                # Check format of token expiration date
                if len(token["expiry"]) == 20:
                    expiration_date = datetime.strptime(token["expiry"], "%Y-%m-%dT%H:%M:%SZ")
                else:
                    expiration_date = datetime.strptime(token["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")

            if current_time > expiration_date:
                # Delete token file
                os.remove(token_path)
            else:
                self.credentials = Credentials.from_authorized_user_file(token_path, self.TOKEN_SCOPES)

        # if not credentials or they're not valid
        if not self.credentials or not self.credentials.valid:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.TOKEN_SCOPES)
            self.credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(self.credentials.to_json())