import unittest
import tempfile
import json
from datetime import datetime

from src import conf
from src.conf import Config

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.file_data = {
            "scenario_data": {
                "last_played": "1999-01-24 7:12:56",
                "playlist_type": "beginner",
                "beginner_scenarios": {
                    "CsLevel.Lowgravity56.VT x WHJ.RWFAP2": "vt x whj smooth strafe sphere easy",
                },
                "intermediate_scenarios": {
                    "CsLevel.Lowgravity56.VT x WHJ.RWEZ9J": "vt x whj smooth strafe sphere",
                }
            },
            "sheets": {
                "id": "random_sheet_id"
            }
        }
    
    def test_read_config(self):
        _, fpath = tempfile.mkstemp(suffix=".json")
        with open(fpath, "w") as jsonFile:
            json.dump(self.file_data, jsonFile)
        self.assertEqual(Config.read_config(fpath), self.file_data)

    def test_config_outputs(self):
        last_played, SHEET_ID, cs_level_ids = Config.parse_config(self.file_data)
        with self.subTest("last_played"):
            # Convert setup time into datetime
            setup_time = datetime.strptime(self.file_data["scenario_data"]["last_played"], "%Y-%m-%d %H:%M:%S")
            self.assertEqual(last_played, setup_time)

        with self.subTest("sheet"):
            self.assertEqual(SHEET_ID, self.file_data["sheets"]["id"])

        with self.subTest("difficulty"):
            self.assertEqual(cs_level_ids, self.file_data["scenario_data"]["beginner_scenarios"])

class TestConfigExceptions(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.file_data = {
            "scenario_data": {
                "last_played": "1999-01-24 7:12:56",
                "playlist_type": "",
                "beginner_scenarios": {
                    "CsLevel.Lowgravity56.VT x WHJ.RWFAP2": "vt x whj smooth strafe sphere easy",
                },
                "intermediate_scenarios": {
                    "CsLevel.Lowgravity56.VT x WHJ.RWEZ9J": "vt x whj smooth strafe sphere",
                }
            },
            "sheets": {
                "id": "random_sheet_id"
            }
        }

    def test_difficulty_exception(self):
        with self.assertRaises(conf.IncorrectDifficultyException):
            Config.parse_config(self.file_data)
        
if __name__ == "__main__":
    unittest.main()