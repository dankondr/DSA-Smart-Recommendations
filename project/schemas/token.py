import re

from pydantic import BaseModel, ConstrainedStr


class Email(ConstrainedStr):
    regex = re.compile('[a-zA-Z.]+@(edu.)?hse.ru')


class TokenData(BaseModel):
    email: Email
