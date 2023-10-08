from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET = os.environ.get("AUTH_SECRET") or "testingsecret123454321"
TOKEN = '6127328784:AAHbn9EDtNJjGGziMJjmBj1KId_gy43CCSE'