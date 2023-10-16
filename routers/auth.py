from fastapi import APIRouter, status, HTTPException, Depends
from passlib.hash import pbkdf2_sha256
from schema.schema import LoginInSchema, TokenData
from database.db import User, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from typing import Annotated
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
router = APIRouter(tags=['Login'])

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if token_data is None:
        raise credentials_exception
    return token_data


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(request: OAuth2PasswordRequestForm = Depends()):
    query = User.select().where(request.username == User.c.username)
    user = await database.fetch_one(query=query)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not pbkdf2_sha256.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    access_token = create_access_token(data={'sub': user.username})
    return {"access_token": access_token, "token_type": "bearer"}
