from pyro_utils import get_all_dialogs, send_message, get_chat_history, download_media
import time
import asyncio
import pyro_settings as ps
from behoof_local import load_json, save_json, calculate_md5
from utils import book_get, get_access_token, book_create, upload_file
from settings import cridentials


if __name__ == "__main__":
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    assert len(access_token) == 331, "Error in `get_access_token`"

    has_been_sent_dct = load_json('data', 'has_been_sent.json', default=[])
    for account in ps.account_list:
        dialog_lst = asyncio.run(get_all_dialogs(account))
        # dialog_lst = asyncio.run(send_message(account,ps.target,"Йа знаю где ты живешь"))
        for dialog in dialog_lst:
            dci = dialog.chat.id
            if str(dci) != ps.target:
                continue
            print('-' * 10)
            message_lst = asyncio.run(get_chat_history(account, ps.target))
            for message in message_lst:
                key = f"{message.chat.id}|{message.id}"
                if key in has_been_sent_dct:
                    continue
                if message.document and message.document.file_name.endswith(".pdf"):
                    ext = message.document.file_name.split('.')[-1]
                    file_message = asyncio.run(download_media(account, message.document.file_id, message.document.file_name))
                    print(message.document)

                    # Загрузка файла
                    book_dct = upload_file(file_message, access_token, govdatahub=cridentials[2])
                    book_id = book_dct.get("id")
                    filename_orig = book_dct.get("filename_orig")

                    # Обновление книги
                    book_dct.update(
                        {
                            'title': message.document.file_name,
                            'telegram_file_id': message.document.file_id,                            
                        }
                    )
                    ret = book_create(book_id, book_dct, access_token, govdatahub=cridentials[2])
                    has_been_sent_dct.append(key)
                    save_json('data', 'has_been_sent.json', has_been_sent_dct)
                    break 
                
                
            # logging.warning(f'{account}|{dci}|{dialog.chat.username}')
            # if dci > 0:
            #     continue
            # if dci in settings.exclude_chats:
            #     continue
            # message_lst = asyncio.run(get_chat_history_new(account, dci, limit=100))
            # for message in message_lst:
            #     key = f"{message.chat.id}|{message.id}"
            #     url = f"https://t.me/{dialog.chat.username}/{message.id}"
            #     if key not in was_sent:
            #         pm = process_message(message, parser_lst, key)
            #         was_sent[key] = pm.get("result", list())                       

            # save_json("data", "account_was_sent.json", account_was_sent)
            # time.sleep(3)