import re
import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError

from database.models import Company
from routes.contracts import router as contracts_router
from schemas.company import CompanyCreate, CompanyResponse

router = APIRouter()
router.include_router(
    contracts_router, prefix="/{company_cnpj}/contracts", tags=["contracts"]
)


@router.get("/", response_model=List[CompanyResponse])
async def read_companies(page: int = 0, page_size: int = 10):
    """
    Lista as empresas cadastradas
    """
    companies = Company.select().offset(page).limit(page_size)
    companies_list = []

    for company in companies:
        company_dict = model_to_dict(company, exclude=[Company.logo])
        company_dict["logo"] = bytes(company.logo)

        companies_list.append(company_dict)

    return companies_list


@router.get("/{company_cnpj}", response_model=CompanyResponse)
async def read_company(company_cnpj: str):
    """
    Retorna os dados de uma empresa específica
    """
    company = Company.get_or_none(Company.cnpj == company_cnpj)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    company_dict = model_to_dict(company, exclude=[Company.logo])
    company_dict["logo"] = bytes(company.logo)

    return company_dict


@router.post("/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate):
    """
    Cria uma nova empresa
    """
    try:
        company_obj = Company.create(
            nickname=company.nickname,
            trade_name=company.trade_name,
            corporate_name=company.corporate_name,
            cnpj=re.sub(r"\D", "", company.cnpj),
            state=company.state,
            city=company.city,
            logo=bytes(company.logo) if company.logo else None,
        )
        return model_to_dict(company_obj)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Company with this CNPJ already exists"
        )


@router.put("/{company_cnpj}", response_model=CompanyResponse)
async def update_company(company: CompanyCreate, company_cnpj: str):
    """
    Atualiza os dados de uma empresa
    """
    company_obj = Company.get_or_none(Company.cnpj == company_cnpj)

    if not company_obj:
        raise HTTPException(status_code=404, detail="Company not found")

    company_obj.nickname = company.nickname
    company_obj.trade_name = company.trade_name
    company_obj.corporate_name = company.corporate_name
    company_obj.state = company.state
    company_obj.city = company.city
    company_obj.logo = bytes(company.logo) if company.logo else None

    company_obj.save()

    company_dict = model_to_dict(company_obj, exclude=[Company.logo])
    company_dict["logo"] = bytes(company.logo)

    return company_dict


@router.delete("/{company_cnpj}", status_code=204)
async def delete_company(company_cnpj: str):
    """
    Deleta uma empresa:
    """
    company = Company.get_or_none(Company.cnpj == company_cnpj)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    company.delete_instance()

    return {"detail": "Company deleted successfully"}
