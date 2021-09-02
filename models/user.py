from datetime import datetime

from passlib.context import CryptContext
from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField, IntegerField

from core.database import Model

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Like(Model):
    project_id = IntegerField()


class User(Model):
    class PasswordComparator:
        __slots__ = 'password_hashed'

        def __init__(self, password_hashed: str) -> None:
            self.password_hashed = password_hashed

        def __eq__(self, password: str) -> bool:
            return pwd_context.verify(password, self.password_hashed)

        def __ne__(self, password: str) -> bool:
            return not (self == password)

    email = CharField(unique=True, index=True)
    password_hashed = CharField()
    registered_date = DateTimeField(default=datetime.now)
    last_authorized = DateTimeField(default=datetime.now)
    disabled: bool = BooleanField(default=False)
    likes = ForeignKeyField(Like, backref='user', on_delete='CASCADE')

    @property
    def password(self) -> str:
        return self.PasswordComparator(self.password_hashed)

    @password.setter
    def password(self, value: str) -> None:
        self.password_hashed = pwd_context.hash(value)

    async def like(self, project_id: int) -> None:
        await Like.manager.create(Like, user=self, project_id=project_id)
