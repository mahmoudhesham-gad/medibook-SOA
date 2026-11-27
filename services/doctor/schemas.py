from datetime import date, datetime, time, timedelta
from typing import Optional

from pydantic import BaseModel


def _format_date(value) -> str:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    return str(value)


def _format_time(value) -> str:
    if isinstance(value, timedelta):
        return (datetime.min + value).strftime("%H:%M")
    if isinstance(value, time):
        return value.strftime("%H:%M")
    return str(value)[:5]


class DoctorResponse(BaseModel):
    doctor_id: int
    name: str
    specialty: str
    consultation_fee: float
    room: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "DoctorResponse":
        return cls(
            doctor_id=data["doctor_id"],
            name=data["name"],
            specialty=data["specialty"],
            consultation_fee=round(float(data["consultation_fee"]), 2),
            room=data.get("room"),
        )


class SlotResponse(BaseModel):
    slot_id: int
    doctor_id: int
    slot_date: str
    start_time: str
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> "SlotResponse":
        return cls(
            slot_id=data["slot_id"],
            doctor_id=data["doctor_id"],
            slot_date=_format_date(data["slot_date"]),
            start_time=_format_time(data["start_time"]),
            status=data["status"],
        )
