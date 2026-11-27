from flask import Blueprint, jsonify, request

import services

bp = Blueprint("doctor", __name__, url_prefix="/api")


@bp.get("/doctors")
def list_doctors():
    specialty = request.args.get("specialty")
    doctors = [d.model_dump() for d in services.list_doctors(specialty)]
    return jsonify(doctors), 200


@bp.get("/doctors/<int:doctor_id>")
def get_doctor(doctor_id):
    return jsonify(services.get_doctor(doctor_id).model_dump()), 200


@bp.get("/doctors/<int:doctor_id>/slots")
def list_doctor_slots(doctor_id):
    slot_date = request.args.get("date")
    slots = [s.model_dump() for s in services.list_doctor_slots(doctor_id, slot_date)]
    return jsonify(slots), 200


@bp.get("/slots/<int:slot_id>")
def get_slot(slot_id):
    return jsonify(services.get_slot(slot_id).model_dump()), 200


@bp.put("/slots/<int:slot_id>/reserve")
def reserve_slot(slot_id):
    return jsonify(services.reserve_slot(slot_id).model_dump()), 200


@bp.put("/slots/<int:slot_id>/release")
def release_slot(slot_id):
    return jsonify(services.release_slot(slot_id).model_dump()), 200
