import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class Config:
    SERVICE_NAME = "doctor"
    PORT = int(os.getenv("PORT", "5002"))
    TEAM_NUMBER = int(os.getenv("TEAM_NUMBER", "0"))  # set to your T

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "clinic_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "clinic_system")
