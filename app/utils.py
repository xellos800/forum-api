from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
import jwt
from .database import engine
from . import models, oauth2
from datetime import datetime, timezone, timedelta

# I. User authentication: getting password hash
# Get a hash of user password at login

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_user(username: str, db: Session):
    query = select(models.User).where(
        models.User.email == username
    )

    user = db.scalars(query).first()

    return user


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user
