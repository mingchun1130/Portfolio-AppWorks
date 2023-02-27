import os

from dotenv import load_dotenv

load_dotenv()
STYLISH_DB_URL = os.getenv("STYLISH_DB_URL")
