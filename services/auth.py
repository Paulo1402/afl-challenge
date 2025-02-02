import os
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from schemas.user import TokenData, UserInDB
from database.models import User as UserModel

from fastapi import Depends, HTTPException, status


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username: str, password: str) -> UserInDB | bool:
    user = UserModel.get_or_none(UserModel.username == username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        data = payload.get("sub")

        if not data:
            raise credentials_exception

        token_data = TokenData(**data)
    except jwt.PyJWTError:
        raise credentials_exception

    return token_data


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token)
