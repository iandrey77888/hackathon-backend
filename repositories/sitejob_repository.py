from typing import List, Optional
from sqlalchemy.orm import Session, Query, joinedload
from models.domain.hack import Job2stage, Sitejob, Users
from core.database import get_db
from services.auth_service import ERole
from datetime import datetime
class SitejobRepository: 
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, sitejob_id: int) -> Optional[Sitejob]:
        return self.db.query(Sitejob).filter(Sitejob.id == sitejob_id).one()
    
    def get_job2stage_by_id(self, sitejob_id: int, stage_id: int) -> Optional[Sitejob]:
        return self.db.query(Job2stage).join(Job2stage.sitejob).filter(Sitejob.id == sitejob_id, Job2stage.stageid == stage_id).one()