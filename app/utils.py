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

# I. User authentication: verifying password
# Verify that hashed password matches what is in database


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

# # I. User authentication and authorization: username
# # Looks for username in database
# # returns user information that in Pydantic model form
# # Used in functions to authenticate user on login or get the current logged in user


def get_user(username: str):
    with Session(engine) as db:
        query = select(models.User).where(
            models.User.email == username)
    # or do I need to use one()? does return None if it doesnt find anything/
    user = db.scalars(query).first()
    return user

# # I. User authentication: Putting user and password authentication together
# #  verify user and password


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password):
        return False
    return user
