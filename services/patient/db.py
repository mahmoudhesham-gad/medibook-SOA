import mysql.connector
from mysql.connector import errors as mysql_errors

from config import Config
from errors import ConflictError, ServiceUnavailableError


def get_connection():
    try:
        return mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
        )
    except mysql_errors.Error:
        raise ServiceUnavailableError("Database is unavailable")


def query_one(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchone()
    finally:
        conn.close()


def execute(sql, params=()):
    """Runs INSERT/UPDATE, commits, returns (rowcount, lastrowid)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount, cur.lastrowid
    finally:
        conn.close()


# ---- patients table (the only table this service touches) ----

def insert_patient(name, email, phone, password_hash, plan_code):
    sql = (
        "INSERT INTO patients (name, email, phone, password_hash, insurance_plan_code) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    try:
        _, new_id = execute(sql, (name, email, phone, password_hash, plan_code))
    except mysql_errors.IntegrityError as e:
        if e.errno == 1062:  # duplicate entry on UNIQUE(email)
            raise ConflictError("Email already registered", code="EMAIL_EXISTS")
        raise
    return new_id


def get_by_id(patient_id):
    return query_one("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))


def get_by_email(email):
    return query_one("SELECT * FROM patients WHERE email = %s", (email,))


def increment_visits(patient_id):
    rowcount, _ = execute(
        "UPDATE patients SET completed_visits = completed_visits + 1 WHERE patient_id = %s",
        (patient_id,),
    )
    return rowcount
