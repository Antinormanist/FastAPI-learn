import datetime as dt
from datetime import datetime, timedelta

from decouple import config
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from app.database import get_db
from app.schemas import Token
from app.models import User
from app.utils import verify_password

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

router = APIRouter(
    tags=['Authentication']
)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(dt.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES if ACCESS_TOKEN_EXPIRE_MINUTES else 60)
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('user_id')
        if id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return id


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    user_id = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'something get wrong. Current authenticated user is not found')
    return user


@router.post('/login', response_model=Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if user is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Invalid credentials')
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Invalid credentials')
    access_token = create_access_token(data={'user_id': user.id, })
    return {'access_token': access_token, 'token_type': 'bearer'}
