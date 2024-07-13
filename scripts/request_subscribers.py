import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest

my_api_id = 25484784
my_api_hash = "b657ccab805ea6d68e944c282f891c39"
my_phone_number = "+79168241245"
my_password = "qwerty120978"
my_url = "t.me/dealwithcaution"

async def request_subscribers(api_id, api_hash, phone_number, url, password=""):
    client = TelegramClient(str(api_id), api_id, api_hash, system_version="4.16.30-vxCUSTOM")

    async def main(phone_number, password, url):
        await sign_in_account(phone_number, password)
        return await get_subscribers(url)
        
    async def get_subscribers(url):
        ch = await client.get_entity(url)
        channel_info = await client(GetFullChannelRequest(channel=ch))
        res_sub = channel_info.full_chat.participants_count
        return res_sub

    async def sign_in_account(phone_number, password):
        await client.start(phone=phone_number, password=password, code_callback=telegram_code_callback)
        
    async def telegram_code_callback():
        code = input("test")
        return code

    
    return await main(phone_number, password, url)

    



