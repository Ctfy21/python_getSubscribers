import asyncio
import threading
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Group, Account

my_api_id = 25484784
my_api_hash = "b657ccab805ea6d68e944c282f891c39"
my_phone_number = "+79168241245"
my_password = "qwerty120978"


# Logic

def request_group(loop, client, url):
    asyncio.set_event_loop(loop)
    while(True):
        if(client == None):
            print("Error during get telegram client!")
            return
        with client:
            res = loop.run_until_complete(get_subscribers(client, url))
        print(res)
        asyncio.sleep(60)
        

def receive_subscribers_from_groups(queue):
    loop = asyncio.get_event_loop()
    client = sign_in_account(queue, my_api_id, my_api_hash, my_phone_number, my_password)
    print(client)
    array_group = get_groups_repository()
    for group in array_group:
        print(group.url)
        threading.Thread(target=request_group, args=(loop, client, group.url)).start()

# DB repository

def get_groups_repository():
    engine = create_engine("sqlite:///instance/main.db")
    Session = sessionmaker(autoflush=False, bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Group).all()


# Telegram Repository

def sign_in_account(queue, api_id, api_hash, phone_number, password=""):

    def get_code_callback():
        return queue.get()
    
    try:
        client = TelegramClient(str(api_id), api_id, api_hash, system_version="4.16.30-vxCUSTOM")
        client.start(phone=phone_number, password=password, code_callback=get_code_callback)  
        return client   
    except Exception as e:
        # print(e)
        return None


async def get_subscribers(client, url):
    ch = await client.get_entity(url)
    channel_info = await client(GetFullChannelRequest(channel=ch))
    res_sub = channel_info.full_chat.participants_count
    return res_sub



        

    



