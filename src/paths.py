import os
import pathlib as p
import sys

# Check if program is python script or exe
if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
    print("Is exe")
    CURR_DIR = p.Path(sys.executable).parent.absolute()
else:
    print("running from python script")
    CURR_DIR = p.Path(__file__).parent.parent.absolute()

CREDENTIALS_PATH = os.path.join(CURR_DIR, "credentials.json")
TOKENS_PATH = os.path.join(CURR_DIR, "tokens.json")
LOGGING_PATH = os.path.join(CURR_DIR, "debug.log")
CONFIG_PATH = os.path.join(CURR_DIR, "config.json")
AIMLAB_DB_PATH = os.path.abspath(os.path.join(os.getenv("APPDATA"), os.pardir, "LocalLow\\statespace\\aimlab_tb\\klutch.bytes"))