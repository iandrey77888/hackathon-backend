from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from geoalchemy2 import Geometry
import core.config as config

engine = create_engine(config.DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()