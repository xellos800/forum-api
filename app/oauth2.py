from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
import datetime
from . import database, models
from .schemas import TokenData
from .config import settings
import jwt
from datetime import timezone, timedelta, datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_MINUTES = settings.expire_minutes


def generate_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY,
                             algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Your credentials could not be verified.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_token(token, credentials_exception)
    user = db.scalars(select(models.User).where(
        models.User.email == token.username)).first()

    return user
