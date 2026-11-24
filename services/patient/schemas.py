from typing import Annotated, Optional
from dataclasses import dataclass

from pydantic import (
    BaseModel,
    BeforeValidator,
    EmailStr,
    Field,
    StringConstraints,
)


def _strip_lower(v):
    return v.strip().lower() if isinstance(v, str) else v


class RegisterRequest(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    email: Annotated[EmailStr, BeforeValidator(_strip_lower)]
    phone: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^01\d{9}$")]
    password: Annotated[str, Field(min_length=6, max_length=128)]
    insurance_plan_code: Optional[str]

class LoginRequest(BaseModel):
    email: Annotated[EmailStr, BeforeValidator(_strip_lower)]
    password: Annotated[str, Field(min_length=6, max_length=128)]

@dataclass(frozen=True)
class PatientResponse:
    patient_id: int
    name: str
    email: str
    phone: str
    insurance_plan_code: Optional[str]
    completed_visits: int

    def from_dict(data: dict) -> "PatientResponse":
        return PatientResponse(
            patient_id=data["patient_id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            insurance_plan_code=data.get("insurance_plan_code"),
            completed_visits=data["completed_visits"],
        )
