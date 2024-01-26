import json
import os
from datetime import datetime

from paths import CONFIG_PATH
from error_logging import parse_error

class IncorrectDifficultyException(Exception): pass

class Config():
    def read_config(file_path):
        if not os.path.isfile(file_path):
            parse_error("config_path")

        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            
        return json_data

    def parse_config(json_data):
        last_played = datetime.strptime(json_data["scenario_data"]["last_played"], "%Y-%m-%d %H:%M:%S")
        SHEET_ID = json_data["sheets"]["id"]
        cs_level_ids = None
        difficulty = json_data["scenario_data"]["playlist_type"].lower()

        match difficulty:
            case "beginner":
                cs_level_ids = json_data["scenario_data"]["beginner_scenarios"]
            case "intermediate":
                cs_level_ids = json_data["scenario_data"]["intermediate_scenarios"]
            case _:
                raise IncorrectDifficultyException
            
        return (last_played, SHEET_ID, cs_level_ids)

    def update_config(file_path, json_data):
        with open(file_path, "w") as jsonFile:
            json.dump(json_data, jsonFile, indent=4, ensure_ascii=False)