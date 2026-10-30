from .. import models, schemas, utils
from ..oauth2 import get_current_user
from ..database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    post_query = select(models.Post).where(models.Post.id == vote.post_id)
    post = db.execute(post_query).scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    vote_query = select(models.Vote).where(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = db.execute(vote_query).scalar_one_or_none()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User has has already liked this post.")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Post liked."}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="You have not liked this post.")
        db.delete(found_vote)
        db.commit()
        return {"message": "You have unliked this post."}
