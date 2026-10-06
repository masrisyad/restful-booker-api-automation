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

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")