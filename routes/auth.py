from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from peewee import IntegrityError

from schemas.user import UserCreate, Token, User
from database.models import User as UserModel
from services.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Realiza a autenticação do usuário e retorna um token de acesso
    """
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": {"username": user.username, "email": user.email}},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado
    """
    return current_user


@router.post("/users/", name="Criar usuário", response_model=User)
async def create_user(user: UserCreate):
    """
    Cria um novo usuário
    """
    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])

    try:
        UserModel.create(**user_dict)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    return user_dict
