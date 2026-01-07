import os
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv("FIREBASE_API_KEY")
EMAIL=os.getenv("FIREBASE_EMAIL")
PASSWORD=os.getenv("FIREBASE_PASSWORD")
APP_URL=os.getenv("FIREBASE_APP_URL")