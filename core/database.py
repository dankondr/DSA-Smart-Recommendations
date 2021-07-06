from peewee import Model as _Model
from peewee_async import Manager
from peewee_asyncext import PooledPostgresqlExtDatabase

from core.settings import settings

Database = PooledPostgresqlExtDatabase

db = Database(None)
db.set_allow_sync(True)  # peewee-migrations
db_manager = Manager(db)
execute = db_manager.execute
db.init(
    database=settings.postgres_db,
    user=settings.postgres_user,
    host=settings.postgres_host,
    password=settings.postgres_password,
    min_connections=1,
    max_connections=settings.postgres_max_conn,
)


async def connect_database() -> None:
    await db_manager.connect()


async def close_database() -> None:
    await db_manager.close()


class Model(_Model):
    manager = db_manager

    class Meta:
        database = db
