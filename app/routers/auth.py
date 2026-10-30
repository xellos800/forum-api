from .. import utils, oauth2
from ..schemas import Token
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = utils.authenticate_user(
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong username or password.")
    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong userame or password.")
    access_token_expires = timedelta(minutes=oauth2.EXPIRE_MINUTES)
    access_token = oauth2.generate_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
