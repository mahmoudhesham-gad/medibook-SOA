from flask import Blueprint, jsonify, request

import services
from errors import ValidationError
from schemas import LoginRequest, RegisterRequest

bp = Blueprint("patients", __name__, url_prefix="/api/patients")



@bp.post("/register")
def register():
    req = RegisterRequest.model_validate(request.get_json())
    return jsonify(services.register_patient(req).model_dump()), 201


@bp.post("/login")
def login():
    req = LoginRequest.model_validate(request.get_json())
    return jsonify(services.login_patient(req)), 200


@bp.get("/<int:patient_id>")
def profile(patient_id):
    return jsonify(services.get_patient(patient_id).model_dump()), 200


@bp.get("/<int:patient_id>/appointments")
def appointments(patient_id):
    return jsonify(services.get_patient_with_appointments(patient_id)), 200


@bp.put("/<int:patient_id>/visits")
def visits(patient_id):
    return jsonify(services.add_visit(patient_id).model_dump()), 200
