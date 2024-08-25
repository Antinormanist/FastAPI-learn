from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import Vote
from app.database import get_db
from app.routers.auth import get_current_user
from app import models

router = APIRouter(
    tags=['Vote']
)

@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote(body: Vote, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if db.query(models.Vote).filter(models.Vote.post_id == body.post_id and models.Vote.user_id == user.id).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'you have voted this post')
    post = db.query(models.PostModel).filter(models.PostModel.id == body.post_id).first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'post with id: {body.post_id} is not found')
    if body.dir:
        post.upvotes += 1
    else:
        post.downvotes += 1
    v = models.Vote(post_id=body.post_id, user_id=user.id)
    db.add(v)
    db.commit()
    db.refresh(v)
    return {'message': 'successfully added vote'}