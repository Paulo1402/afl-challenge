import datetime

from peewee import *


db = PostgresqlDatabase('afl-challenge', user='postgres', password='postgres', host='localhost', port=5432)


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

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)


class Contract(BaseModel):
    company = ForeignKeyField(Company, backref='contracts', on_delete='CASCADE')
    effective_date = DateField()
    signature_date = DateField()
    contract_rate = FloatField(),
    contracted_services = CharField()


class Department(BaseModel):
    name = CharField()


class Service(BaseModel):
    contract = ForeignKeyField(Contract, backref='services')
    department = ForeignKeyField(Department, backref='services')
    service_type = CharField()


def initialize_departments():
    Department.get_or_create(name='Departamento A')
    Department.get_or_create(name='Departamento B')


db.connect()
db.create_tables([Company, Contract, Department, Service])
initialize_departments()
db.close()
