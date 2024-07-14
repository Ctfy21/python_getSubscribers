from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata = metadata)

class Group(Base):
    __tablename__ = "Group"

    id = Column(Integer, primary_key=True)
    url = Column(String(200), unique=True, nullable=False)
    subscribers = Column(Integer, nullable=True)

    def __init__(self, url):
        self.url = url

class Account(Base):
    __tablename__ = "Account"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(80), unique=True, nullable=False)
    api_id = Column(String(80), unique=False, nullable=False)
    api_hash = Column(String(200), unique=False, nullable=False)
    password = Column(String(200), unique=False, nullable=True)

    def __init__(self, phone_number, api_id, api_hash, password):
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash
        self.password = password
