import os

from sqlalchemy import  Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

PG_USER = os.getenv("PG_USER", "user")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1234")
PG_DB = os.getenv("PG_DB", "async")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5431")

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class SwapiPeople(Base):
    __tablename__ = "swapi_people"
    id = Column(Integer, primary_key=True)
    birth_year = Column(String(10))
    eye_color = Column(String(20))
    films = Column(String(1000))
    gender = Column(String(10))
    hair_color = Column(String(20))
    height = Column(String(10))
    homeworld = Column(String(100))
    mass = Column(String(10))
    name = Column(String(100))
    skin_color = Column(String(20))
    species = Column(String(500))
    starships = Column(String(500))
    vehicles = Column(String(500))
