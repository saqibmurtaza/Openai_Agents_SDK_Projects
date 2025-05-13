from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or ""
MODEL_NAME = os.getenv("MODEL_NAME") or ""
SHEET_ID = os.getenv("SHEET_ID")  # Load Sheet ID
SHEET_NAME = os.getenv("SHEET_NAME", "Living Room Products")  # Load Sheet Name
