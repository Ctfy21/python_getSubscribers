from telethon.tl.functions.channels import GetFullChannelRequest

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