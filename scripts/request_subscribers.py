import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

my_api_id = 25484784
my_api_hash = "b657ccab805ea6d68e944c282f891c39"
my_phone_number = "+79168241245"
my_password = "qwerty120978"


# Logic

def request_group(loop, client, url):
    asyncio.set_event_loop(loop)
    while(True):
        time.sleep(60)
        if(client != None):
            with client:
                res = loop.run_until_complete(get_subscribers(client, url))
            print(res)

def receive_subscribers_from_groups(queue, loop):
    client = sign_in_account(queue, my_api_id, my_api_hash, my_phone_number, my_password)
    session = create_session()
    print(session.query())



# DB Repository
def create_session():
    engine = create_engine("sqlite:///main.db", echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


# Telegram Repository

def sign_in_account(queue, api_id, api_hash, phone_number, password=""):

    def get_code_callback():
        return queue.get()

    try:
        client = TelegramClient(str(api_id), api_id, api_hash, system_version="4.16.30-vxCUSTOM")
        client.start(phone=phone_number, password=password, code_callback=get_code_callback)  
        return client   
    except:
        return None
    


async def get_subscribers(client, url):
    ch = await client.get_entity(url)
    channel_info = await client(GetFullChannelRequest(channel=ch))
    res_sub = channel_info.full_chat.participants_count
    return res_sub



        

    



