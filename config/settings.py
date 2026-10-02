import os

from dotenv import load_dotenv


load_dotenv()


BASE_URL = os.getenv(
    "BASE_URL",
    "https://restful-booker.herokuapp.com",
)

API_USERNAME = os.getenv("API_USERNAME")

API_PASSWORD = os.getenv("API_PASSWORD")

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "30")
)