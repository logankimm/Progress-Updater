import pathlib
import json
import os
import sqlite3
import sys
import time
from datetime import datetime
import urllib.request
import csv
import logging
from google_apis.sheets import Sheets_API

# Create Google API to do stuff with
def initalize_apis(spread_id, *args):
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    # When there is pre-determined credentials/token path already
    sheet = Sheets_API(scopes = SCOPES, ID = spread_id)
    return sheet

def parse_config():
    try:
        with open("./config.json", "r") as json_file:
            json_data = json.load(json_file)
        
        last_played = datetime.strptime(json_data["scenario_data"]["last_played"], "%Y-%m-%d %H:%M:%S")
        SHEET_ID = json_data["sheets"]["id"]
        cs_level_ids = None

        # Match scenario difficulty
        difficulty = json_data["scenario_data"]["playlist_type"].lower()
        match difficulty:
            case "beginner":
                cs_level_ids = json_data["scenario_data"]["beginner_scenarios"]
            case "intermediate":
                cs_level_ids = json_data["scenario_data"]["intermediate_scenarios"]
            case _:
                raise ValueError
        logging.info("Config.json has been parsed incorrectly")

    except:
        logging.info("Error while parsing config file")
        raise ValueError
    return (json_data, last_played, SHEET_ID, cs_level_ids)


def parse_query(result):
    error_offset, parsed_values = 0, []

    # iterate through in chunks of 3
    for i in range(len(result)):

        # Every 3 indicies create an interval for the day
        if (i % 3) == 2 - error_offset:
            errors = 0
            # Check if dates of beginning and end of interval have same date
            if result[i - 2][1][:10] != result[i][1][:10]:
                errors += 1
                # Check if middle scenario was also corrupted
                if result[i - 2][1][:10] != result[i - 1][1][:10]:
                    errors += 1
                
                # Update error offset
                error_offset += errors
                
            # Compute the intervals for the day
            row_data = result[i - 2:i + 1 - errors]
            scores = [x[0] for x in row_data]
            parsed_values.append(scores)
        
    return parsed_values

def update_config(json_data):
    with open("config.json", "w") as jsonFile:
        json.dump(config_data, jsonFile, indent=4, sort_keys=True)

if __name__ == "__main__":
    # initialize global variables
    SHEET_ID = ""
    CURR_ROW = ""
    PREV_PLAYED = ""
    AIMLAB_DB_PATH = os.path.abspath(os.path.join(os.getenv("APPDATA"), os.pardir, "LocalLow\\statespace\\aimlab_tb\\klutch.bytes"))

    # Parse config file and update proper variables
    config_data, PREV_PLAYED, SHEET_ID, cs_level_ids = parse_config()
    sheet = initalize_apis(spread_id = SHEET_ID)

    # Open db connection
    try:
        con = sqlite3.connect(AIMLAB_DB_PATH)
        cur = con.cursor()
        logging.info("SQL Connection Successful")
    except:
        logging.info("Failure to connect SQL database - no solution for this one chief except pray")
        raise ValueError

    # Get scores from the database
    for scenario_index, item in enumerate(cs_level_ids.items()):
        csid, name = item
        
        # Query for new data to add
        cur.execute(
            f"SELECT score, endedAt FROM TaskData WHERE taskName = ? AND endedAt > date(?) ORDER BY endedAt",
            [csid, PREV_PLAYED])
        result = cur.fetchall()

        # Update the last played within config file
        config_data["scenario_data"]["last_played"] = result[-1][1]
        update_config(config_data)

        update_data = parse_query(result)
        
        # Update Sheet
        sheet.update_scenario(update_data, scenario_index, len(update_data))
        
    logging.info("Log for current day successful")