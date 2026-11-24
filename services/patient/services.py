from werkzeug.security import check_password_hash, generate_password_hash

import clients
import db
from errors import InvalidCredentialsError, NotFoundError
from schemas import PatientResponse


def register_patient(req):
    if req.insurance_plan_code:
        clients.get_plan(req.insurance_plan_code)  # 400 if unknown, 503 if down

    new_id = db.insert_patient(
        req.name,
        req.email,
        req.phone,
        generate_password_hash(req.password),
        req.insurance_plan_code,
    )
    return PatientResponse.from_dict(db.get_by_id(new_id))


def login_patient(req):
    row = db.get_by_email(req.email)
    # Same error for unknown email and wrong password: don't reveal which.
    if not row or not check_password_hash(row["password_hash"], req.password):
        raise InvalidCredentialsError("Wrong email or password")
    return {"patient_id": row["patient_id"], "name": row["name"]}


def get_patient(patient_id):
    row = db.get_by_id(patient_id)
    if not row:
        raise NotFoundError(f"Patient {patient_id} not found")
    return PatientResponse.from_dict(row)


def get_patient_with_appointments(patient_id):
    profile = get_patient(patient_id).model_dump()  # 404 first
    profile["appointments"] = clients.list_appointments(patient_id)  # 503 if down
    return profile


def add_visit(patient_id):
    if db.increment_visits(patient_id) == 0:
        raise NotFoundError(f"Patient {patient_id} not found")
    return get_patient(patient_id)
