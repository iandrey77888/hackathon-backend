from typing import List, Optional
from sqlalchemy.orm import Session
from models.domain.hack import Files, Users
from core.database import get_db

class FilesRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, file_id: int) -> Optional[Files]:
        return self.db.query(Files).filter(Files.id == file_id).one()
    
    def add_new(self, comm: Files):
        self.db.add(comm)
        self.db.commit()