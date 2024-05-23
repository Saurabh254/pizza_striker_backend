from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from api.database import db
from api.utils.auth import auth

from . import interface, models, schemas

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login", response_model=schemas.LoginResponse)
async def login(data: schemas.LoginUser, db: Session = Depends(db.get_db)):
    try:
        return interface.user_login(
            phone=data.phone, hashed_password=data.hashed_password, db=db
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=schemas.SlimUser)
async def get_me(current_user: Annotated[models.Users, Depends(auth.get_current_user)]):
    return current_user


@router.get("/leaderboard", response_model=Page[schemas.SlimUser])
async def get_leaderboard(db: Session = Depends(db.get_db)):
    try:
        return interface.get_leaderboard(db=db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
