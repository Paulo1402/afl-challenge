from datetime import timedelta

import dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from companies import router as companies_router

from auth import get_password_hash, verify_password, create_access_token, get_current_user
from schemas import UserCreate, Token, UserInDB, User


dotenv.load_dotenv()

app = FastAPI(root_path="/api")

app.include_router(companies_router, prefix='/companies', tags=['companies'], dependencies=[Depends(get_current_user)],)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": get_password_hash("secret"),
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": {
            "username": user.username,
            "email": user.email

        }}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)

    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return UserInDB(**user)


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    user_dict = user.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    fake_users_db[user.username] = user_dict
    return user_dict
