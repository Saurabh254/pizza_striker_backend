from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path, Query
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from api.database.db import get_db
from api.routes.users import interface as users_interface
from api.routes.users import schemas as users_schemas
from api.utils.auth import auth

from . import errors, interface, models, schemas

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=schemas.LoginResponse)
async def login(data: schemas.LoginUser, db: Session = Depends(get_db)):
    try:
        return interface.admin_login(
            phone=data.phone, hashed_password=data.hashed_password, db=db
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent_strikes", response_model=Page[users_schemas.StrikesResponse])
async def get_strikes(
    admin: Annotated[models.Admins, Depends(auth.get_current_admin)],
    db: Session = Depends(get_db),
):
    try:
        return interface.get_recent_strikes(db=db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users", response_model=Page[users_schemas.FullUser])
async def get_users(
    admin: Annotated[models.Admins, Depends(auth.get_current_admin)],
    db: Session = Depends(get_db),
):
    try:
        return interface.get_users(db=db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_strike", response_model=users_schemas.StrikesResponse)
async def create_user_strike(
    admin: Annotated[models.Admins, Depends(auth.get_current_admin)],
    data: schemas.CreateStrike,
    db: Session = Depends(get_db),
):
    try:
        return interface.create_user_strike(data=data, db=db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_strike", status_code=204)
async def delete_user_strike(
    admin: Annotated[models.Admins, Depends(auth.get_current_admin)],
    strike_id: Annotated[str, Query(min_length=12, max_length=12)],
    db: Session = Depends(get_db),
):
    try:
        return interface.delete_user_strike(strike_id, db=db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=None)
async def get_user_by_id(
    admin: Annotated[models.Admins, Depends(auth.get_current_admin)],
    user_id: Annotated[str, Path(max_length=12, min_length=12)],
    db: Session = Depends(get_db),
):
    try:
        return interface.get_user_by_id(user_id=user_id, db=db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
