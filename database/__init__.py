from .models import *
from services.auth import get_password_hash


def initialize_departments():
    Department.get_or_create(name="Departamento A")
    Department.get_or_create(name="Departamento B")


def initialize_services():
    Service.get_or_create(name="COMPRA")
    Service.get_or_create(name="VENDA")
    Service.get_or_create(name="TROCA")


def initialize_users():
    User.get_or_create(username="afl", email="test@afl.com", password=get_password_hash("afl123"))


def init_db():
    db.connect()

    db.drop_tables([Company, Contract, Department, Service, ContractService, User])
    db.create_tables([Company, Contract, Department, Service, ContractService, User])

    initialize_departments()
    initialize_services()
    initialize_users()

    db.close()
