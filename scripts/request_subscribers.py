import multiprocessing
import os
import sys
import time

from sqlalchemy import create_engine
from telethon import TelegramClient

from db_repository import get_groups_repository, set_group_subscribers_repository
from telegram_repository import get_subscribers, send_subscribers_to_result_send_chat

def main_receive_cycle(queue, accounts):

    print("come to main_receive_cycle")

    res_array = []
    for account in accounts:

        def get_code_callback():
            return queue.get()
        
        client = TelegramClient(str(account.api_id), account.api_id, account.api_hash, system_version="4.16.30-vxCUSTOM")
        client.start(phone=account.phone_number, password=account.password, code_callback=get_code_callback)

        res_array.append([account, client])

        if(client.is_connected()):
            print(f"Client: {account.phone_number} - ready")
        else:
            os.execv(sys.executable, ['python'] + sys.argv)
    
        client.disconnect()
    
    for res_val in res_array:
        multiprocessing.Process(target=receive_subscribers_from_groups, args=(res_val[0],), daemon=True).start()
        print(f"Client: {res_val[0].phone_number} - start")
        time.sleep(2)
    
    



def receive_subscribers_from_groups(account):

    client = TelegramClient(str(account.api_id), account.api_id, account.api_hash, system_version="4.16.30-vxCUSTOM")
    engine = create_engine("sqlite:///instance/main.db")

    print("come to receive_subscribers_from_groups")

    while(True):
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
        time.sleep(5)




        

    



