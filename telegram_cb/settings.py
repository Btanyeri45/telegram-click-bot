from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent

API_ID = config("API_ID")

API_HASH = config("API_HASH")
