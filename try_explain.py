from utils import get_access_token, book_update, book_upload, book_download, author_post, add_author_to_book
import os


ret = get_access_token("user1", "password1", govdatahub="govdatahub.ru")
access_token = ret.get("access_token")
assert len(access_token) == 331, "Error in `get_access_token`"

# Загрузить книги
pth = "/media/pascal65536/1TB/Books/"
for root, dirs, files in os.walk(pth):
    for f in files[-5:-1]:
        ret = get_access_token("user1", "password1", govdatahub="govdatahub.ru")
        access_token = ret.get("access_token")
        assert len(access_token) == 331, "Error in `get_access_token`"    

        book_path = os.path.join(root, f)
        if book_path.endswith(".pdf"):
            ret = book_upload(book_path, access_token, govdatahub="govdatahub.ru")
            print(ret)
            print('-' * 20)


# Скачивание книги
# book_id = '00200207ac63c070c5a77ef27356509f'
# ret = book_download(book_id, access_token, govdatahub="govdatahub.ru")
# assert ret.status_code == 200, "Error in `book_download`"


# # Сохранение файла на диск
# os.makedirs("_download", exist_ok=True)
# filename_orig = 'Вейдман_С_Глубокое_обучение_Легкая_разработка_проектов_на_Python.pdf'
# file_path = os.path.join("_download", filename_orig)
# with open(file_path, "wb") as f:
#     f.write(ret.content)
# assert os.path.exists(file_path) is True,  "Error in `f.write(ret.content)`"


# Добавление автора
# json_data = {"name": "Сет Вейдман"}
# ret = author_post(json_data, access_token, govdatahub="govdatahub.ru")
# author_id = ret.get("id")
# print(author_id)


# Добавление автора в список авторов книги
# book_id = '00200207ac63c070c5a77ef27356509f'
# author_id = 1
# ret = add_author_to_book(book_id, author_id, access_token, govdatahub="govdatahub.ru")
# print(ret)



# Обновление книги
# book_id = '00200207ac63c070c5a77ef27356509f'
# json_data = {
#     "title": "Глубокое обучение: легкая разработка проектов на Python",
#     "isbn": "ISBN 978-5-4461-1675-1",
#     "publication_date": "2021",
#     "publisher": "СПб.: Питер",
#     "description": '''Взрывной интерес к нейронным сетям и искусственному интеллекту затронул уже все об-
# ласти жизни, и понимание принципов глубокого обучения необходимо каждому разработчику
# ПО для решения прикладных задач. Эта практическая книга представляет собой вводный курс
# для всех, кто занимается обработкой данных, а также для разработчиков ПО. Вы начнете с ос-
# нов глубокого обучения и быстро перейдете к более сложным архитектурам, создавая проекты
# с нуля. Вы научитесь использовать многослойные, сверточные и рекуррентные нейронные
# сети. Только понимая принцип их работы (от «математики» до концепций), вы сделаете свои
# проекты успешными. В этой книге:
# xx Четкие схемы, помогающие разобраться в нейросетях, и примеры рабочего кода.
# xx Методы реализации многослойных сетей с нуля на базе простой объектно-ориентированной
# структуры.
# xx Примеры и доступные объяснения сверточных и рекуррентных нейронных сетей.
# xx Реализация концепций нейросетей с помощью популярного фреймворка PyTorch.''',
# } 
# ret = book_update(book_id, json_data, access_token, govdatahub="govdatahub.ru")
# print(ret)