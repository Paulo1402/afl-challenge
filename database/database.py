from peewee import PostgresqlDatabase

from libs.utils import settings


db = PostgresqlDatabase(
    settings.postgres_db,
    user=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=settings.postgres_port,
)
