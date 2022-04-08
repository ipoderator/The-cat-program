""" Вариант той же программы только в асинхронном варианте, отработала за 1,4 секунды """

import requests
from time import time # Для того что-бы засикать время выполнения программы 

import asyncio
import aiohttp # Делаем импорт для работы по протоколу http
""" Все запросы лучше делать через сессию,так написанно в документации к aiohttp """

""" Синхронная функция имя будем определять по unix времени, отбросив всю дробную часть """

def write_image(data):
    filename = 'file-{}.jpeg'.format(int(time() * 1000))
    with open(filename, 'wb') as file:
        file.write(data)


""" Функция fetch_content принимает 2 аргумента url - по которому мы делаем запрос и session - сессия.  
            Когда мы работаем с сессиями, нужно использовать контекстный менеджер """    

async def fetch_content(url, session):
    async with session.get(url, allow_redirects = True) as response:
        data = await response.read()
        
        """ Метод read возвращяет бинарные данные, т.е картинку, которая будет записана в переменную data """ 

        write_image(data)


async def main2():
    url = 'https://loremflickr.com/320/240'
    tasks = [] 

    """ Для того что бы корутина попала в очередь задач её нужно обернуть в task,
     но что бы не создавать 10 раз одно и тоже, создаём контейнер tasks """
    
    """ Открываем сессию и 10 раз вызываем функцию fetch_content """

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session)) 
            tasks.append(task) # Task записываем в контейнер tasks

        """ Дожидаемся окончания работы корутин, т.е вызвать метод gather"""

        await asyncio.gather(*tasks) # '*' означает, что список tasks будет распакован 


if __name__ == '__main__':
    t0 = time() # Засикаем время
    asyncio.run(main2())
    print(time() - t0)