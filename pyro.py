from pyro_utils import get_all_dialogs, send_message
import time
import asyncio
import settings
#как запостить файл
if __name__ == "__main__":
    for account in settings.account_list:
        # dialog_lst = asyncio.run(get_all_dialogs(account))
        dialog_lst = asyncio.run(send_message(account,settings.target,"Йа знаю где ты живешь"))
        
        # for dialog in dialog_lst:
        #     dci = dialog.chat.id
        #     print(str(dci)==settings.target)
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