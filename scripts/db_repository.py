from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata = metadata)

class Group(Base):
    __tablename__ = "Group"

    id = Column(Integer, primary_key=True)
    url = Column(String(200), unique=True, nullable=False)
    subscribers = Column(Integer, nullable=True)

    def __init__(self, url, subscribers):
        self.url = url
        self.subscribers = subscribers

class Account(Base):
    __tablename__ = "Account"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(80), unique=True, nullable=False)
    api_id = Column(String(80), unique=False, nullable=False)
    api_hash = Column(String(200), unique=False, nullable=False)
    password = Column(String(200), unique=False, nullable=True)
    result_send_chat = Column(String(200), unique=False, nullable=False)

    def __init__(self, phone_number, api_id, api_hash, password, result_send_chat):
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash
        self.password = password
        self.result_send_chat = result_send_chat

def get_groups_repository(engine):
    Session = sessionmaker(autoflush=False, bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Group).all()

def get_accounts_repository(engine):
    Session = sessionmaker(autoflush=False, bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Account).all()

def set_group_subscribers_repository(engine, group_url, subs):
    Session = sessionmaker(autoflush=False, bind=engine)
    try:
        with Session(autoflush=False, bind=engine) as db:
            group = db.query(Group).filter_by(url=group_url).first()
            group.subscribers = subs
            db.add(group)
            db.commit()
            return True
    except:
        return False
