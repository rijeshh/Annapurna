# apps/api/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env file

DATABASE_URL = os.getenv("DATABASE_URL")

# establishes the connection to PostgreSQL
engine = create_engine(DATABASE_URL)

# factory for creating sessions per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# parent class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass