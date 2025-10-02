from typing import List, Optional
from sqlalchemy import String, cast, func, text
from sqlalchemy.orm import Session, Query, joinedload
from models.domain.hack import Buildsite, Users
from core.database import get_db
from services.auth_service import ERole
from datetime import datetime
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
class BuildsiteRepository: 
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, buildsite_id: int) -> Optional[Buildsite]:
        return self.db.query(Buildsite).filter(Buildsite.id == buildsite_id).one()

    def get_by_id_details(self, buildsite_id: int) -> Optional[Buildsite]:
        return self.db.query(Buildsite).options(joinedload('*')).filter(Buildsite.id == buildsite_id).one()
    
    def get_by_role(self, cur_user:Users) -> Query[Buildsite]:
        match cur_user.role:
            case ERole.CONTRACTOR:
                return self.db.query(Buildsite).order_by(
                    Buildsite.start_date.desc()).filter(
                        (Buildsite.manager == cur_user.id) | (Buildsite.start_date > datetime.now()))
            case _:
                return self.db.query(Buildsite).join(Buildsite.users).where(Users.id == cur_user.id)

    def user_has_perms(self, cur_user:Users, buildsite_id:int) -> bool:
        match cur_user.role:
            case ERole.CONTRACTOR:
                return self.db.query(Buildsite).filter(Buildsite.id == buildsite_id, Buildsite.manager == cur_user.id).scalar() is not None
            case ERole.INSPECTOR:
                return self.db.query(Buildsite).join(Buildsite.users).filter(Buildsite.id == buildsite_id, Users.id == cur_user.id).scalar() is not None
            case _:
                return False
    
    def point_on_site(self, buildsite_id: int, longitude: float,  latitude: float, precision: float):
        return (
        self.db.query(Buildsite)
        .filter(
            Buildsite.id == buildsite_id,
            text(f"ST_DWithin(Buildsite.coordinates::geography, ST_MakePoint({longitude}, {latitude}), {precision})")
        )
        .one_or_none()
        )   