from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SenateMember(Base):
    __tablename__ = 'senate'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    img_url = Column(String)
    party = Column(String)
    birth_date = Column(String)
    city = Column(String)
    com_const = Column(String)
    twitter = Column(String)
