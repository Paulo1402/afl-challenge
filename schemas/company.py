import datetime
from typing import Optional

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    nickname: str
    trade_name: str
    corporate_name: str
    cnpj: str
    state: str
    city: str
    logo: Optional[bytes]


class CompanyResponse(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    nickname: str
    trade_name: str
    corporate_name: str
    cnpj: str
    state: str
    city: str
    logo: Optional[bytes]
