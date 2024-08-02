import datetime
from typing import List

from pydantic import BaseModel, field_validator


class ServiceDepartmentRequest(BaseModel):
    service: str
    department: str


class ContractRequest(BaseModel):
    effective_date: datetime.datetime
    signature_date: datetime.datetime
    contract_rate: float
    services: List[ServiceDepartmentRequest]

    @field_validator("effective_date", "signature_date", mode="before")
    @classmethod
    def parse_dates(cls, date: str):
        return datetime.datetime.strptime(date, "%d-%m-%Y")


class ContractResponse(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    effective_date: datetime.datetime
    signature_date: datetime.datetime
    contract_rate: float
    services: List[ServiceDepartmentRequest]

    @field_validator("effective_date", "signature_date", mode="after")
    @classmethod
    def parse_dates(cls, date: datetime.datetime):
        return date.strftime("%d-%m-%Y")
