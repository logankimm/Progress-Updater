import json
import os
import sys
import logging
import sqlite3
from datetime import datetime
from google_apis.sheets import Sheets_API

def close_program():
    input("Press enter to close program")
    sys.exit(1)

# Create Google API to do stuff with
def initalize_apis(spread_id, *args):
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
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

        logging.info("Config.json has been parsed correctly")

    except ValueError as err:
        logging.warning("Scenario difficulty has been incorrectly input")
        close_program()

    except:
        logging.exception("Error while parsing config file")
        close_program()
        
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
        json.dump(config_data, jsonFile, indent=4, ensure_ascii=False,)

if __name__ == "__main__":
    logging.basicConfig(
        level = logging.WARNING,
        format = "%(asctime)s %(levelname)s %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [
            logging.FileHandler("debug.log"),
            logging.StreamHandler("sys.stdout")
        ],
    )

    # initialize global variables
    SHEET_ID = ""
    CURR_ROW = ""
    PREV_PLAYED = ""
    try:
        AIMLAB_DB_PATH = os.path.abspath(os.path.join(os.getenv("APPDATA"), os.pardir, "LocalLow\\statespace\\aimlab_tb\\klutch.bytes"))
    except:
        logging.error("Aimlabs file path does not exist")
        close_program

    # Parse config file and update proper variables
    config_data, PREV_PLAYED, SHEET_ID, cs_level_ids = parse_config()

    try:
        sheet = initalize_apis(spread_id = SHEET_ID)
    except:
        logging.exception("Error while creating instance of Google API")
        input("Press enter to exit")
        sys.exit(1)

    # Open db connection
    try:
        con = sqlite3.connect(AIMLAB_DB_PATH)
        cur = con.cursor()
        logging.info("SQL Connection Successful")
    except:
        logging.exception("Failure to connect SQL database - no solution for this")
        close_program

    try:
        # Get scores from the database
        for scenario_index, item in enumerate(cs_level_ids.items()):
            csid, name = item
            
            # Query for new data to add
            cur.execute(
                f"SELECT score, endedAt FROM TaskData WHERE taskName = ? AND endedAt > DATETIME(?) ORDER BY endedAt",
                [csid, PREV_PLAYED])
            result = cur.fetchall()

            # Update the last played within config file
            config_data["scenario_data"]["last_played"] = result[-1][1]
            update_config(config_data)

            update_data = parse_query(result)
            
            # Update Sheet
            sheet.update_scenario(update_data, scenario_index, len(update_data))
    except:
        logging.exception("Error while parsing query_data")
        close_program()

    logging.info("Log for current day successful")