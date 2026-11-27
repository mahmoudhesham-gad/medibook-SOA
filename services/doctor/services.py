from datetime import datetime

import db
from errors import ConflictError, NotFoundError, ValidationError
from schemas import DoctorResponse, SlotResponse


def list_doctors(specialty=None):
    cleaned = specialty.strip() if isinstance(specialty, str) else None
    rows = db.list_doctors(cleaned or None)
    return [DoctorResponse.from_dict(row) for row in rows]


def get_doctor(doctor_id):
    row = db.get_doctor_by_id(doctor_id)
    if not row:
        raise NotFoundError(f"Doctor {doctor_id} not found")
    return DoctorResponse.from_dict(row)


def list_doctor_slots(doctor_id, slot_date=None):
    get_doctor(doctor_id)  # 404 if doctor does not exist

    parsed_date = None
    if slot_date is not None and slot_date.strip():
        date_str = slot_date.strip()
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("date must be in YYYY-MM-DD format")

    rows = db.list_available_slots(doctor_id, parsed_date)
    return [SlotResponse.from_dict(row) for row in rows]


def get_slot(slot_id):
    row = db.get_slot_by_id(slot_id)
    if not row:
        raise NotFoundError(f"Slot {slot_id} not found")
    return SlotResponse.from_dict(row)


def reserve_slot(slot_id):
    if db.reserve_slot(slot_id) == 0:
        if not db.get_slot_by_id(slot_id):
            raise NotFoundError(f"Slot {slot_id} not found")
        raise ConflictError(
            f"Slot {slot_id} is already booked", code="SLOT_NOT_AVAILABLE"
        )
    return get_slot(slot_id)


def release_slot(slot_id):
    if db.release_slot(slot_id) == 0:
        if not db.get_slot_by_id(slot_id):
            raise NotFoundError(f"Slot {slot_id} not found")
        raise ConflictError(
            f"Slot {slot_id} is not booked", code="INVALID_STATUS"
        )
    return get_slot(slot_id)
