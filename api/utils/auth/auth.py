from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.database import db
from api.routes.admin import interface as admins_interface
from api.routes.users import interface as users_interface
from api.routes.users import models as users_model

from .auth_bearer import JWTBearer

# to get a string like this run:
# openssl rand -hex 32

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, phone: str, password: str):
    user = users_interface.get_user(phone=phone, db=db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    payload_data: Annotated[str, Depends(JWTBearer())], db: Session = Depends(db.get_db)
):
    phone = payload_data["phone"]
    role = payload_data["role"]
    hashed_password = payload_data["hashed_password"]
    user = users_interface.get_user(phone=phone, hashed_password=hashed_password, db=db)
    if not user or role != "User":
        raise HTTPException(
            status_code=404,
            detail=f"user not found with the phone number asssociated with {phone}",
        )

    return user


async def get_current_admin(
    payload_data: Annotated[str, Depends(JWTBearer())], db: Session = Depends(db.get_db)
):
    phone = payload_data["phone"]
    role = payload_data["role"]
    hashed_password = payload_data["hashed_password"]
    admin = admins_interface.get_admin(
        phone=phone, hashed_password=hashed_password, db=db
    )
    if not admin:
        raise HTTPException(
            status_code=404,
            detail=f"user not found with the phone number asssociated with {phone}",
        )

    return admin
