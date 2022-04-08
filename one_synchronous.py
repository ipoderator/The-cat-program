""" Пишем программу для скачивания рандомных 10 картинок с котиками. 
Одна программа будет выполняться синхронно, а другая асинхронно 
и тем самым можно будет посмотреть , какая из этих 2-х программ 
будет работать быстрее, отработала за 3,8 секунды """


import requests
from time import time # Для того что-бы засикать время выполнения программы 


url = 'https://loremflickr.com/320/240'


def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r 


def write_file(response):
    filename = response.url.split('/')[-1] # Берем из url последний элемент 
    with open(filename, 'wb') as file: # Отрываем файловый объект для записи бинарных данных ("wb")
        file.write(response.content)


def main():
    t0 = time() # Засикаем время

    url = 'https://loremflickr.com/320/240'

    for i in range(10): # 10 раз вызываем функцию write
        write_file(get_file(url))

    print(time() - t0) # Показывает сколько времени занимает выполн. программы


if __name__ == '__main__':
    main()




