from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.domain.hack import Comment2file, Comments, Users, Buildsite
from core.database import get_db
from services.auth_service import ERole

class CommentsRepository: 
    def __init__(self, db: Session):
        self.db = db

    def get_active_comments(self, site: Buildsite):
        return self.db.query(Comments).join(Comments.buildsite).where(Comments.state == 0).where(Buildsite.id == site.id)
    
    def get_active_notes_cnt(self, site: Buildsite):
        return self.db.query(func.count()).select_from(Comments).join(Comments.buildsite).filter(Comments.state == 0,Comments.rec_type == 0, Buildsite.id == site.id).scalar()
    
    def get_active_warns_cnt(self, site: Buildsite):
        return self.db.query(func.count()).select_from(Comments).join(Comments.buildsite).filter(Comments.state == 0,Comments.rec_type == 1, Buildsite.id == site.id).scalar()

    def add_new(self, comm: Comments):
        self.db.add(comm)
        self.db.commit()

    def link_file(self, comm: Comments, file_id: int):
        link_obj = Comment2file(notice = comm.id, file = file_id)
        self.db.add(link_obj)
        self.db.commit()