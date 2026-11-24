import requests

from config import Config
from errors import ServiceUnavailableError, ValidationError


def _get(url, service):
    try:
        return requests.get(url, timeout=Config.REQUEST_TIMEOUT)
    except requests.RequestException:
        raise ServiceUnavailableError(f"{service} service is unavailable")


def get_plan(plan_code):
    """Billing: GET /api/billing/plans/{plan_code}. Unknown plan -> 400 (per spec)."""
    response = _get(f"{Config.BILLING_URL}/api/billing/plans/{plan_code}", "Billing")
    if response.status_code == 404:
        raise ValidationError(f"Insurance plan '{plan_code}' not found")
    if response.status_code != 200:
        raise ServiceUnavailableError("Billing service returned an error")
    return response.json()


def list_appointments(patient_id):
    """Appointment: GET /api/appointments?patient_id=..."""
    response = _get(
        f"{Config.APPOINTMENT_URL}/api/appointments?patient_id={patient_id}",
        "Appointment",
    )
    if response.status_code != 200:
        raise ServiceUnavailableError("Appointment service returned an error")
    return response.json()
