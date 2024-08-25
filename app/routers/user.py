from typing import List

from fastapi import HTTPException, status, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/', response_model=List[schemas.UserReturn])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get('/{user_id}', response_model=schemas.UserReturn)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'user with id: {user_id} is not found')
    return user


@router.post('/', response_model=schemas.UserReturn, status_code=status.HTTP_201_CREATED)
def create_user(body: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == body.username).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'user with such username already exists')
    if db.query(models.User).filter(models.User.email == body.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'user with such email already exists')
    body.password = utils.hash_it(body.password)
    user = models.User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put('/{user_id}', response_model=schemas.UserReturn)
def update_user(user_id: int, body: schemas.UserUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_db = db.query(models.User).filter(models.User.id == user_id)
    if user_db.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'user with id: {user_id} is not found')
    if user_db.first().username != user.username:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'you must be authenticated as this user to change its info')
    if db.query(models.User).filter(models.User.username == body.username).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'user with such username already exists')
    if db.query(models.User).filter(models.User.email == body.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, 'user with such email already exists')
    user_db.update(body.dict(), synchronize_session=False)
    db.commit()
    return user_db.first()


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_db = db.query(models.User).filter(models.User.id == user_id).first()
    if user_db is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'user with id: {user_id} is not found')
    if user_db.username != user.username:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'you must be authenticated as this user to delete it')
    db.delete(user_db)
    db.commit()