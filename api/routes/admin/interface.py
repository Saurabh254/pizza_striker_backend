from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from api.utils.auth import auth_bearer
from . import errors, models, schemas

from api.routes.users import interface as user_interface
from api.routes.users import models as user_models


def get_admin(phone: str, hashed_password: str, db: Session):
    phone = "+91" + phone if len(phone) == 10 else phone
    return (
        db.query(models.Admins)
        .filter(
            models.Admins.phone == phone,
            models.Admins.hashed_password == hashed_password,
        )
        .scalar()
    )


def admin_login(phone: str, hashed_password: str, db: Session):
    phone = "+91" + phone if len(phone) == 10 else phone
    admin = get_admin(phone=phone, hashed_password=hashed_password, db=db)

    if not admin:
        raise errors.AdminNotFoundError(phone=phone)
    data = {
        "id": admin.id,
        "phone": admin.phone,
        "hashed_password": admin.hashed_password,
        "role": "Admin",
    }
    access_token = auth_bearer.create_access_token(data=data)
    return {"access_token": access_token, "admin": admin}


def get_recent_strikes(db: Session):
    query = db.query(user_models.UserStrikes).order_by(
        user_models.UserStrikes.created_at.desc()
    )
    return paginate(db, query)


def get_users(db: Session):
    query = db.query(user_models.Users).order_by(user_models.Users.strike_count.desc())
    return paginate(db, query)


def get_user_by_id(user_id: str, db: Session) -> user_models.Users | None:
    return db.query(user_models.Users).filter(user_models.Users.id == user_id).scalar()


def create_user_strike(data: schemas.CreateStrike, db: Session):
    user = get_user_by_id(user_id=data.user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="user does not exists")
    strike = user_models.UserStrikes(user_id=data.user_id, reason=data.reason)
    user.strike_count = user.strike_count + 1
    db.add(strike)
    db.commit()
    db.refresh(strike)
    db.refresh(user)
    return strike


def delete_user_strike(strike_id: str, db: Session):
    strike: user_models.UserStrikes | None = (
        db.query(user_models.UserStrikes)
        .filter(user_models.UserStrikes.id == strike_id)
        .scalar()
    )
    if strike:
        user = db.get(user_models.Users, strike.user_id)
        user.strike_count = user.strike_count - 1 if user.strike_count > 0 else 0
        db.commit()
        db.refresh(user)

    db.delete(strike)
    db.commit()
