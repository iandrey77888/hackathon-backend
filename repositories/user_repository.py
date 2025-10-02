# app/repositories/user_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from models.domain.hack import Users
from core.database import get_db

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[Users]:
        return self.db.query(Users).filter(Users.id == user_id).one()
    
    def get_by_username(self, username: str) -> Optional[Users]:
        return self.db.query(Users).filter(Users.username == username).one()
    
    def create(self, user_data: dict) -> Users:
        db_user = Users(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, update_data: dict) -> bool:
        result = self.db.query(Users).filter(Users.id == user_id).update(update_data)
        self.db.commit()
        return result > 0