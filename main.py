from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.sessions import StringSession

my_api_id = 25484784
my_api_hash = "b657ccab805ea6d68e944c282f891c39"
phone_number="+79168241245"

client = TelegramClient('anon', my_api_id, my_api_hash, system_version="4.16.30-vxCUSTOM")

client.start(phone_number)

async def main():
    ch = await client.get_entity("@dealwithcaution")
    result = await client(GetFullChannelRequest(channel=ch))
    print(result.stringlify())

with client:
    client.loop.run_until_complete(main())