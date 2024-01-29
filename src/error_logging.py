import logging
import sys

error_list = {
    "config_difficulty": "Make sure difficulty has been changed in config file",
    "config_general": "Config file error: ",
    "config_path":"Config file not found. Please make sure it exists",
    "credentials_dne": "credentials.json file doesn't exist. Try again",
    "google_api": "Google API Error: ",
    "sheets_api": "Sheets API Error: ",
    "sheets_update": "Error while updating sheet: ",
    "SQL_connection": "Couldn't connect to local database. No solution for this",
    "undefined": "An undefined error occured. Please send submit an issue to github"
}

def parse_error(error, error_text = None):
    error_msg = error_list.get(error, "undefined")
    if error_text:
        error_msg += error_text
        
    logging.error(error_msg)
    input("Press enter to quit")
    sys.exit(1)