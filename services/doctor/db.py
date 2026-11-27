import mysql.connector
from mysql.connector import errors as mysql_errors

from config import Config
from errors import ServiceUnavailableError


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


def query_all(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
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


# ---- doctors & slots tables (the only tables this service touches) ----

def list_doctors(specialty=None):
    if specialty:
        return query_all(
            "SELECT doctor_id, name, specialty, consultation_fee, room "
            "FROM doctors WHERE LOWER(specialty) = LOWER(%s) ORDER BY doctor_id",
            (specialty,),
        )
    return query_all(
        "SELECT doctor_id, name, specialty, consultation_fee, room "
        "FROM doctors ORDER BY doctor_id"
    )


def get_doctor_by_id(doctor_id):
    return query_one(
        "SELECT doctor_id, name, specialty, consultation_fee, room "
        "FROM doctors WHERE doctor_id = %s",
        (doctor_id,),
    )


def list_available_slots(doctor_id, slot_date=None):
    if slot_date is not None:
        return query_all(
            "SELECT slot_id, doctor_id, slot_date, start_time, status "
            "FROM slots "
            "WHERE doctor_id = %s AND status = 'AVAILABLE' AND slot_date = %s "
            "ORDER BY slot_date ASC, start_time ASC",
            (doctor_id, slot_date),
        )
    return query_all(
        "SELECT slot_id, doctor_id, slot_date, start_time, status "
        "FROM slots "
        "WHERE doctor_id = %s AND status = 'AVAILABLE' "
        "ORDER BY slot_date ASC, start_time ASC",
        (doctor_id,),
    )


def get_slot_by_id(slot_id):
    return query_one(
        "SELECT slot_id, doctor_id, slot_date, start_time, status "
        "FROM slots WHERE slot_id = %s",
        (slot_id,),
    )


def reserve_slot(slot_id):
    """Atomically reserve an AVAILABLE slot; returns affected rowcount."""
    rowcount, _ = execute(
        "UPDATE slots SET status = 'BOOKED' WHERE slot_id = %s AND status = 'AVAILABLE'",
        (slot_id,),
    )
    return rowcount


def release_slot(slot_id):
    """Atomically release a BOOKED slot; returns affected rowcount."""
    rowcount, _ = execute(
        "UPDATE slots SET status = 'AVAILABLE' WHERE slot_id = %s AND status = 'BOOKED'",
        (slot_id,),
    )
    return rowcount
