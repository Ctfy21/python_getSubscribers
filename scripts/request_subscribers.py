import os
import sys
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Group, Account
# Logic

def receive_subscribers_from_groups(queue):

    print("come to receive_subscribers_from_groups")

    engine = create_engine("sqlite:///instance/main.db")
    while(True):
        account = get_account_repository(engine)
        if(account != None):
            break
        time.sleep(1) 


    def get_code_callback():
        return queue.get()

    client = TelegramClient(str(account.api_id), account.api_id, account.api_hash, system_version="4.16.30-vxCUSTOM")
    client.start(phone=account.phone_number, password=account.password, code_callback=get_code_callback)

    while(True):
        if(queue.full()):
            os.execv(sys.executable, ['python'] + sys.argv)
        groups = [group for group in get_groups_repository(engine)]
        for group in groups:
            res_sub = None
            with client:
                res_sub = client.loop.run_until_complete(get_subscribers(client, group.url))
            if(res_sub != group.subscribers):
                set_subs_db_flag = set_group_subscribers_repository(engine, group.url, res_sub)
                if(group.subscribers != None and set_subs_db_flag):

                    print(f"Update subs in {group.url}: {res_sub}")

                    res_alg = False
                    with client:
                        res_alg = client.loop.run_until_complete(send_subscribers_to_result_send_chat(client, group.url, account.result_send_chat, group.subscribers, res_sub))

                    if(res_alg):
                        print(f"Отправлено сообщение в result_chat")
                    else:
                        print(f"Что-то не так при отправке сообщения в result_chat")

        time.sleep(60)



# DB repository

def get_groups_repository(engine):
    Session = sessionmaker(autoflush=False, bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Group).all()

def get_account_repository(engine):
    Session = sessionmaker(autoflush=False, bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Account).first()

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

async def send_subscribers_to_result_send_chat(client, url, result_chat, old_subs, new_subs):
    try:
        fin_message = f"{url} - Было: {old_subs} --> Стало: {new_subs}"
        await client.send_message(result_chat, fin_message)
        return True
    except:
        return False



        

    



