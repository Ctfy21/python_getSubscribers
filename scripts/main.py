import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest

my_api_id = 25484784
my_api_hash = "b657ccab805ea6d68e944c282f891c39"
phone_number="+79168241245"

client = TelegramClient('anon', my_api_id, my_api_hash, system_version="4.16.30-vxCUSTOM")

async def get_subscribers(url):
    ch = await client.get_entity(url)
    result = await client(GetFullChannelRequest(channel=ch))
    print(result.stringlify())


async def sign_in_account():
    await client.sign_in(phone_number)
    code = input('enter code: ')
    await client.sign_in(phone_number, code)

    await get_subscribers("t.me/dealwithcaution")

asyncio.run(sign_in_account())

