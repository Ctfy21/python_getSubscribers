from app import run_server
from request_subscribers import request_subscribers
import asyncio
import time

my_api_id = 25484784
my_api_hash = "b657ccab805ea6d68e944c282f891c39"
my_phone_number = "+79168241245"
my_password = "qwerty120978"
my_url = "t.me/dealwithcaution"

def main():
    asyncio.run(request_sub_loop())
    run_server()


async def request_sub_loop():
    while(True):
        res = asyncio.run(request_subscribers(my_api_id, my_api_hash, my_phone_number, my_url, my_password))
        print(res)
        asyncio.sleep(60)



