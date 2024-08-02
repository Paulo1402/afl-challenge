import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from peewee import IntegrityError

from schemas.contract import ContractResponse, ContractRequest
from database.models import Contract, ContractService, Company, Service, Department
from database.models import db

router = APIRouter()


@router.get("/", response_model=List[ContractResponse])
async def get_company_contracts(company_cnpj: str, page: int = 0, page_size: int = 10):
    """
    Retorna os contratos da empresa
    """
    contracts = (
        Contract.select()
        .where(Contract.company == company_cnpj)
        .offset(page)
        .limit(page_size)
    )
    response_data = []

    for contract in contracts:
        contract_services = ContractService.select().where(
            ContractService.contract == contract
        )

        services = []

        for contract_service in contract_services:
            service_name = contract_service.service.name
            department_name = contract_service.department.name
            services.append({"service": service_name, "department": department_name})

        (
            response_data.append(
                ContractResponse(
                    id=contract.id,
                    created_at=contract.created_at,
                    updated_at=contract.updated_at,
                    effective_date=contract.effective_date,
                    signature_date=contract.signature_date,
                    contract_rate=contract.contract_rate,
                    services=services,
                )
            )
        )

    return response_data


@router.post("/", response_model=ContractResponse)
async def create_contract(company_cnpj: str, contract_request: ContractRequest):
    """
    Cria um novo contrato para a empresa
    """
    company = Company.get_or_none(Company.cnpj == company_cnpj)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    with db.atomic() as transaction:
        try:
            contract = Contract.create(
                company=company,
                effective_date=contract_request.effective_date,
                signature_date=contract_request.signature_date,
                contract_rate=contract_request.contract_rate,
            )

            for service_department in contract_request.services:
                service = Service.get_or_none(
                    Service.name == service_department.service
                )
                department = Department.get_or_none(
                    Department.name == service_department.department
                )

                if not service or not department:
                    raise HTTPException(
                        status_code=404, detail="Service or Department not found"
                    )

                ContractService.create(
                    contract=contract, service=service, department=department
                )
        except IntegrityError:
            transaction.rollback()
            raise HTTPException(status_code=400, detail="Contract already exists")
        except Exception:
            transaction.rollback()
            raise
        else:
            transaction.commit()

    return ContractResponse(
        id=contract.id,
        created_at=contract.created_at,
        updated_at=contract.updated_at,
        effective_date=contract.effective_date,
        signature_date=contract.signature_date,
        contract_rate=contract.contract_rate,
        services=contract_request.services,
    )
