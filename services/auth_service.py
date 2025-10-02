from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.hash import argon2
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import core.database as database
import models.domain.hack as m
import core.config as config
from functools import wraps
import inspect
from repositories import user_repository as urepo 

class ERole():
    CONTRACTOR = 0
    FOREMAN = 1
    INSPECTOR  = 2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.TOKEN_URL)

class AuthService():
    def __init__(self, user_repository: urepo.UserRepository):
        self.user_repository = user_repository

    # Hash a new password before saving to DB
    def hash_password(self, password: str) -> str:
        return argon2.hash(password)

    # Verify a password against the stored hash
    def verify_password(self, password: str, hashed: str) -> bool:
        return argon2.verify(password, hashed)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


    def authenticate_user(self, username: str, password: str) -> m.Users:
        try:
            user = self.user_repository.get_by_username(username)
            #user = db.query(m.Users).filter(m.Users.username == username).one()
        except NoResultFound:
            return None
        if not self.verify_password(password, user.pwdhash):
            return None
        return user


    def login_for_access_token(self, form_data: OAuth2PasswordRequestForm):
        if not self.authenticate_user(form_data.username, form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def get_current_user(self, token: str):
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
            try:
                user = self.user_repository.get_by_username(username)
                #user = db.query(m.Users).filter(m.Users.username == username).one()
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )
            
            return user
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    
    

    @staticmethod
    def dec_check_roles(roles: list[int]):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                current_user: m.Users = kwargs.get('current_user')
                
                if current_user.role not in roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid role",
                    )
                if inspect.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            return wrapper
        return decorator