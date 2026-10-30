from .. import models, schemas, utils
from ..oauth2 import get_current_user
from ..database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response

router = APIRouter(prefix="/posts", tags=["Comment"])


@router.post("/{post_id}/comments", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def comment(post_id: int, comment: schemas.CommentCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Find post
    search = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = search.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found!")
    new_comment = models.Comment(
        user_id=current_user.id, post_id=post_id, content=comment.content)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get("/{post_id}/comments", response_model=schemas.CommentWrapper)
def get_comments(post_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.scalar(select(models.Post).where(models.Post.id == post_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    comments = db.scalars(select(models.Comment).where(
        models.Comment.post_id == post_id)).all()
    if not comments:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="No comments found for the specified post id.")

    return {"post": post, "comments": comments}


@router.delete("/{post_id}/comments/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(post_id: int, id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    query = select(models.Comment).where(
        models.Comment.post_id == post_id, models.Comment.id == id)
    comment = db.execute(query).scalar_one_or_none()
    if comment == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment does not exist.")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform this action.")
    db.delete(comment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
