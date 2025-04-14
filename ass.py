import asyncio
import random
from datetime import datetime
from utils_async import APISession


# Задача 1: Асинхронная загрузка данных
async def download_data(url):
    print(f"Начало загрузки {url} в {datetime.now().time()}")
    await asyncio.sleep(random.uniform(0.5, 2))  # Имитация загрузки
    print(f"Завершена загрузка {url} в {datetime.now().time()}")
    return f"Данные с {url}"


# Задача 2: Асинхронная обработка данных
async def process_data(data):
    print(f"Начало обработки данных: {data} в {datetime.now().time()}")
    await asyncio.sleep(random.uniform(0.3, 1.5))  # Имитация обработки
    result = f"Обработанные {data}"
    print(f"Завершена обработка: {result} в {datetime.now().time()}")
    return result


# Задача 3: Асинхронное сохранение данных
async def save_data(data):
    print(f"Начало сохранения данных: {data} в {datetime.now().time()}")
    await asyncio.sleep(random.uniform(0.2, 1))  # Имитация сохранения
    print(f"Завершено сохранение: {data} в {datetime.now().time()}")
    return True


# Основная асинхронная функция
async def main1():
    api_session = APISession("http://govdatahub.ru/")

    access_token = await api_session.get_access_token("user1", "password1")
    assert len(access_token) == 331, "Error in `get_access_token`"

    parallel_tasks = [
        api_session.books_get(),
        api_session.categories_get(),
        api_session.category_get(1),
        api_session.upload_file("fixtures/1.pdf"),
        api_session.upload_file("fixtures/1.png"),
        api_session.download_file("3091401a1c74bfd441ace8d420f1e524.pdf", "1.pdf"),
        api_session.download_file("926d51b67bd5143a49f70513bef45952.png", "1.pdf"),
        api_session.authors_get(),
        api_session.author_get(2),        
    ]

    results = await asyncio.gather(*parallel_tasks)
    for res in results:
        print(res)

    await api_session.close()
    print("Done")    


async def main():
    api_session = APISession("http://govdatahub.ru/")

    access_token = await api_session.get_access_token("user1", "password1")
    assert len(access_token) == 331, "Error in `get_access_token`"

    tasks = [
        asyncio.create_task(api_session.upload_file("fixtures/1.pdf")),
        asyncio.create_task(api_session.upload_file("fixtures/1.png")),        
        asyncio.create_task(api_session.book_get('c78844812d07a05aa01cab0253dce1c7')),
        asyncio.create_task(api_session.author_get(2)),
        asyncio.create_task(api_session.category_get(1)),        
        asyncio.create_task(api_session.download_file("3091401a1c74bfd441ace8d420f1e524.pdf", "2.pdf")),
        asyncio.create_task(api_session.download_file("926d51b67bd5143a49f70513bef45952.png", "2.pdf")),
        asyncio.create_task(api_session.books_get()),
        asyncio.create_task(api_session.authors_get()),
        asyncio.create_task(api_session.categories_get()),
    ]

    # Ожидаем завершения задач и получаем результаты
    for task in tasks:
        result = await task
        # print(f"{result=} {datetime.now().time()}")

    await api_session.close()
    print("Done")    


# Запускаем асинхронные задачи
if __name__ == "__main__":
    asyncio.run(main())
