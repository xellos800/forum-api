from .. import models, schemas
from ..database import get_db
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Response, APIRouter
from typing import List
from ..oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostWrapper])
def get_posts(search: str | None = None, current_user: str = Depends(get_current_user), db: Session = Depends(get_db), limit: int = 20, skip: int = 0):
    vote_count = (
        select(models.Vote.post_id, func.count(
            models.Vote.user_id).label("likes"))
        .group_by(models.Vote.post_id)
        .subquery()
    )
    comment_count = (
        select(models.Comment.post_id, func.count(
            models.Comment.id).label("comments"))
        .group_by(models.Comment.post_id)
        .subquery()
    )
    query = (

        select(models.Post,
               func.coalesce(vote_count.c.likes, 0).label("likes"),
               func.coalesce(comment_count.c.comments, 0).label("comments")
               )

        .outerjoin(vote_count,
                   models.Post.id == vote_count.c.post_id)

        .outerjoin(comment_count,
                   models.Post.id == comment_count.c.post_id)
    )
    if search:
        query = query.where(
            models.Post.title.contains(search)
        )
    results = db.execute(query.limit(limit).offset(skip)).all()

    return [
        {
            "post": post,
            "likes": likes,
            "comments": comments
        }
        for post, likes, comments in results
    ]


@router.get("/{id}", response_model=schemas.PostWrapper)
def get_post(id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    vote_count = (
        select(models.Vote.post_id, func.count(
            models.Vote.user_id).label("likes"))
        .group_by(models.Vote.post_id)
        .subquery()
    )
    comment_count = (
        select(models.Comment.post_id, func.count(
            models.Comment.id).label("comments"))
        .group_by(models.Comment.post_id)
        .subquery()
    )
    query = (
        select(models.Post,
               func.coalesce(vote_count.c.likes, 0).label("likes"),
               func.coalesce(comment_count.c.comments, 0).label("comments")
               )
        .outerjoin(vote_count,
                   models.Post.id == vote_count.c.post_id)

        .outerjoin(comment_count,
                   models.Post.id == comment_count.c.post_id)
        .where(models.Post.id == id)
    )
    result = db.execute(query).one_or_none()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: '{id}' not found!")
    post, likes, comments = result

    return {"post": post,
            "comments": comments,
            "likes": likes}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=schemas.Post)
def update_post(post: schemas.PostCreate, id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.execute(select(models.Post).where(models.Post.id == id))
    found_post = query.scalar_one_or_none()
    if found_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    if found_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform this action.")
    found_post.title = post.title
    found_post.content = post.content
    db.commit()
    db.refresh(found_post)

    return found_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    query = select(models.Post).where(models.Post.id == id)
    post = db.execute(query).scalar_one_or_none()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found!")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform this action.")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
