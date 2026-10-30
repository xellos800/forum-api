from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hash_pwd = utils.get_password_hash(user.password)
    query = db.execute(select(models.User).where(
        models.User.email == user.email))
    found_email = query.scalar_one_or_none()
    if found_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email address already exists")
    new_user = models.User(email=user.email, password=hash_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    find_user = db.execute(select(models.User).where(
        models.User.id == id))
    user = find_user.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    return user
