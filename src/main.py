import json
import os
import sys
import logging
import sqlite3
from datetime import datetime

from sheets import Sheets_API
from paths import AIMLAB_DB_PATH, CREDENTIALS_PATH, TOKENS_PATH, CONFIG_PATH
from error_logging import parse_error
from conf import Config, IncorrectDifficultyException

def parse_query(result):
    error_offset, parsed_values = 0, []

    # Return data as is if length of result < 3
    if len(result) < 3:
        parsed_values.append([x[0] for x in result])
        return parsed_values

    for i in range(len(result)):
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
                
            # Compute the intervals for the day (last 3 scenarios)
            row_data = result[i - 2:i + 1 - errors]
            scores = [x[0] for x in row_data]
            parsed_values.append(scores)
        
    return parsed_values


if __name__ == "__main__":
    logging.basicConfig(
        level = logging.ERROR,
        format = "%(asctime)s %(levelname)s %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [
            logging.FileHandler("debug.log"),
            logging.StreamHandler("sys.stdout")
        ],
    )

    try:
        config_data = Config.read_config(CONFIG_PATH)
        PREV_PLAYED, SHEET_ID, cs_level_ids = Config.parse_config(config_data)
    except FileNotFoundError:
        parse_error("config_path")
    except IncorrectDifficultyException:
        parse_error("config_difficulty")
    except Exception as err:
        parse_error("config_general")
    logging.info("Config data successfully parsed")

    sheet = Sheets_API(ID = SHEET_ID)
    logging.info("Successfully created Sheet API instance")

    try:
        con = sqlite3.connect(AIMLAB_DB_PATH)
        cur = con.cursor()
    except:
        parse_error("SQL_connection")
    logging.info("SQL Connection Successful")

    for scenario_index, item in enumerate(cs_level_ids.items()):
        csid, name = item
        cur.execute(
            f"SELECT score, endedAt FROM TaskData WHERE taskName = ? AND endedAt > DATETIME(?) ORDER BY endedAt",
            [csid, PREV_PLAYED])
        result = cur.fetchall()

        if not result:
            logging.warning("No valid scenario data to add")
            sys.exit(1)
        
        update_data = parse_query(result)
        try:
            sheet.update_scenario(update_data, scenario_index, len(update_data))
        except Exception as err:
            parse_error("sheets_update", err)

    # Update the last played variable within config file
    config_data["scenario_data"]["last_played"] = result[-1][1]
    Config.update_config(CONFIG_PATH, config_data)
    logging.info("Log for current day successful")