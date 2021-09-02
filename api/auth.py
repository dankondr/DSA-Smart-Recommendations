from datetime import datetime, timedelta

from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette import status

from core.settings import settings
from models.user import User
from project.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class Token(BaseModel):
    access_token: str
    token_type: str


class EmailPasswordRequestForm:
    def __init__(
        self,
        email: str = Form(...),
        password: str = Form(...),
    ):
        self.email = email
        self.password = password


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.hashing_algorithm
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.hashing_algorithm]
        )
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await User.manager.get(User, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
