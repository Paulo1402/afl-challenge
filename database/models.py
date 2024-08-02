import datetime

from peewee import *

from database.database import db


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if self._pk is not None:
            self.updated_at = datetime.datetime.now()

        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = db


class Company(BaseModel):
    nickname = CharField()
    trade_name = CharField()
    corporate_name = CharField()
    cnpj = CharField(unique=True)
    state = CharField(max_length=2)
    city = CharField()
    logo = BlobField()


class Contract(BaseModel):
    company = ForeignKeyField(
        Company, field="cnpj", backref="contracts", on_delete="CASCADE"
    )
    effective_date = DateField()
    signature_date = DateField()
    contract_rate = FloatField()


class Department(BaseModel):
    name = CharField()


class Service(BaseModel):
    name = CharField()


class ContractService(BaseModel):
    contract = ForeignKeyField(
        Contract, backref="contract_services", on_delete="CASCADE"
    )
    service = ForeignKeyField(Service, backref="contract_services")
    department = ForeignKeyField(Department, backref="contract_services")

    class Meta:
        database = db
        indexes = ((("contract", "service", "department"), True),)


class User(BaseModel):
    username = CharField()
    email = CharField(unique=True)
    password = CharField()

