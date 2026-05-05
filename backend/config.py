from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://geoflation:geoflation@db:5432/geoflation"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)