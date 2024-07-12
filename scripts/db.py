from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session


sqlite_database = "sqlite:///main.db"


class Base(DeclarativeBase): pass

class Account(Base):
    __tablename__ = "Account"

    id = Column(Integer, primary_key=True, index=True)
    api_id = (Integer,)
    api_hash = (String)
    phone_number = (String)

class Group(Base):
    __tablename__ = "Group"

    id = Column(Integer, primary_key=True, index=True)
    url = (String)


engine = create_engine(sqlite_database)
Base.metadata.create_all(bind=engine)


def add_group(url):
    with Session(autoflush=True, bind=engine) as db:
        group = Group(url=url)
        db.add(group)
        db.commit()

def add_account(api_id, api_hash, phone_number):
    with Session(autoflush=True, bind=engine) as db:
        account = Account(api_id=api_id, api_hash=api_hash, phone_number=phone_number)
        db.add(account)
        db.commit()



