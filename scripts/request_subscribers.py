import asyncio
import threading
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Group, Account
import multiprocessing

my_api_id = 25484784
my_api_hash = "b657ccab805ea6d68e944c282f891c39"
my_phone_number = "+79168241245"
my_password = "qwerty120978"


# Logic

def receive_subscribers_from_groups(queue):

    print("come to receive_subscribers_from_groups")

    engine = create_engine("sqlite:///instance/main.db")

    def get_code_callback():
        return queue.get()

    client = TelegramClient(str(my_api_id), my_api_id, my_api_hash, system_version="4.16.30-vxCUSTOM")
    client.start(phone=my_phone_number, password=my_password, code_callback=get_code_callback)

    while(True):
        groups = [group for group in get_groups_repository(engine)]
        for group in groups:
            with client:
                res = client.loop.run_until_complete(get_subscribers(client, group.url))
                if(res != group.subscribers):
                    if(set_group_subscribers_repository(engine, group.url, res)):
                        print(f"Update subs in {group.url}: {res}")
                        
                    else:
                        print(f"Something worg while update subs in {group.url}")
        time.sleep(60)



# DB repository

def get_groups_repository(engine):
    Session = sessionmaker(autoflush=False, bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Group).all()

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

        
# Telegram repository

async def get_subscribers(client, url):
    ch = await client.get_entity(url)
    channel_info = await client(GetFullChannelRequest(channel=ch))
    res_sub = channel_info.full_chat.participants_count
    return res_sub



        

    



