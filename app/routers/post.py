from typing import List, Optional

from fastapi import HTTPException, status, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.PostReturn])
def get_posts(db: Session = Depends(get_db), page: int = 1, search: Optional[str] = ''):
    if page < 1:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'page mist be greater then 0')
    limit = 10
    skip = limit * (page - 1)
    return db.query(models.PostModel).filter(models.PostModel.is_published == True).filter(models.PostModel.title.icontains(search)).limit(limit).offset(skip)


@router.get('/own', response_model=List[schemas.PostReturn])
def get_own_posts(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return db.query(models.PostModel).filter(models.PostModel.owner_id == user.id)


@router.get('/{post_id}', response_model=schemas.PostReturn)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id == post_id).first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'post with id: {post_id} is not found')
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturn)
def create_posts(body: schemas.PostCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post = models.PostModel(owner_id=user.id, **body.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put('/{post_id}', response_model=schemas.PostReturn)
def update_post(post_id: int, body: schemas.PostUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post = db.query(models.PostModel).filter(models.PostModel.id == post_id)
    user = db.query(models.User).filter(models.User.id == user.id).first()
    if post.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'post with id: {post_id} is not found')
    if post.first().owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'post with id: {post_id} is not your post')
    post.update(body.dict(), synchronize_session=False)
    db.commit()
    return post.first()


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post = db.query(models.PostModel).filter(models.PostModel.id == post_id).first()
    user = db.query(models.User).filter(models.User.id == user.id).first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'post with id: {post_id} is not found')
    if post.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'post with id: {post_id} is not your post')
    db.delete(post)
    db.commit()