from pyrogram import Client
import pyro_settings as ps


api_id = ps.api_id
api_hash = ps.api_hash


async def download_media(my_account, file_id, file_name):
    """
    Download a file.
    """
    try:
        async with Client(my_account, api_id, api_hash) as app:
            file = await app.download_media(file_id, file_name=file_name)
        return file
    except Exception as err:
        print(err)


async def send_message(my_account, chat_id, text):
    """
    Send text messages.
    """
    try:
        async with Client(my_account, api_id, api_hash) as app:
            chat = await app.send_message(chat_id, text)
        return chat
    except Exception as err:
        print(err)

async def get_chat(my_account, chat_id):
    """
    Get up to date information about a chat.
    """
    try:
        async with Client(my_account, api_id, api_hash) as app:
            chat = await app.get_chat(chat_id)
        return chat
    except Exception as err:
        print(err)


async def join_chat(my_account, chat_id):
    """
    Join a group chat or channel.
    """
    print(chat_id)
    async with Client(my_account, api_id, api_hash) as app:
        await app.join_chat(chat_id)
    return


async def get_all_dialogs(my_account):
    """
    Iterate through all
    """
    dialog_lst = list()
    async with Client(my_account, api_id, api_hash) as app:
        async for dialog in app.get_dialogs():
            dialog_lst.append(dialog)
    return dialog_lst


async def get_members(my_account, chat_id):
    """
    Get members
    """
    member_lst = list()
    async with Client(my_account, api_id, api_hash) as app:
        async for member in app.get_chat_members(chat_id):
            member_lst.append(member)
    return member_lst


async def get_chat_history(my_account, chat_id, limit=100):
    """
    Get chat history
    """
    message_lst = list()
    async with Client(my_account, api_id, api_hash) as app:
        async for message in app.get_chat_history(chat_id, limit=limit):
            message_lst.append(message)
    return message_lst


async def forward_messages(my_account, chat_id, from_chat_id, message_ids):
    """
    Forward messages of any kind.
    """
    try:
        async with Client(my_account, api_id, api_hash) as app:
            chat = await app.forward_messages(chat_id, from_chat_id, message_ids)
        return chat
    except Exception as err:
        print(err)


async def copy_messages(my_account, chat_id, from_chat_id, message_ids):
    """
    Copy messages of any kind.
    """
    try:
        async with Client(my_account, api_id, api_hash) as app:
            chat = await app.copy_message(chat_id, from_chat_id, message_ids)
        return chat
    except Exception as err:
        print(err)
