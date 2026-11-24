import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SERVICE_NAME = "patient"
    PORT = int(os.getenv("PORT", "5004"))
    TEAM_NUMBER = int(os.getenv("TEAM_NUMBER", "0"))  # set to your T

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "clinic_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "clinic_system")

    BILLING_URL = os.getenv("BILLING_URL", "http://localhost:5003")
    APPOINTMENT_URL = os.getenv("APPOINTMENT_URL", "http://localhost:5001")
    REQUEST_TIMEOUT = 3
