from select import select
import socket 
from loguru import logger


""" Способ который сейчас будет применяться, для того что-бы добиться асинхронности предложил
Dabid Beazley в 2015 году на PyCon его название 'Concurrency from the Ground up Live'.
В данном примере я преобразовал функцию в генераторы и эти генераторы отдают нам кортежи,
где первый элемент кортежа - это фильтрующий признак по которому мы определяем куда пойдет сокет, который 
находится во втором элементе кортежа. Он пойдет либо на чтение, либо на запись """


tasks = [] # Список с задачами 

to_read = {} # Словарь для хранения сокетов и генераторов
to_write = {} # Словарь для чтения


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Обслуживает запросы клиента 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    """ Устанавливаем таймаут 1 секунду, что бы использовать повторно один и тот же порт """ 
    server_socket.bind(('localhost', 5000))
    server_socket.listen() # Слушает входящие подключения 


    while True:

        yield ('read', server_socket) # Отдает нам серверный сокет 
        client_socket, addr = server_socket.accept()
        
        print('Connection from', addr) 
        """ Принимает входящее подключения, читает данные из входящего буфера,
        если есть подключение, то он возращает кортеж и возвращает клиентский сокет и адресс """
        
        tasks.append(client(client_socket)) # Клиентский сокет добавляем в список tasks


def client(client_socket):
    while True:

        yield ('read', client_socket)
        # Дожидаемся от клиента сообщения  
        request = client_socket.recv(4096) # Принимаем от клиента сообщение 

        """ В цикле прерываем соединение, если ничего не пришло или пишем соотвествующий , если нам что-то пришло """
        if not request:
            break
        else:
            response = 'Hellow maaan\n'.encode()

            yield ('write', client_socket)
            client_socket.send(response)
    
    client_socket.close()


def event_loop(): # Событийный цикл 

    while any([tasks, to_read, to_write]): 
        # Принимает в себя несколько значений которые дают bool значение
        
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, []) # В данную функцию передаем списки(словари), за которыми нам нужно следить  
            
            for sock in ready_to_read: # Обрабатываем списки
                tasks.append(to_read.pop(sock)) # Нужно наполнить список tasks генераторами

            for sock in ready_to_write: # Обрабатываем списки
                tasks.append(to_write.pop(sock)) # Нужно наполнить список tasks генераторами
        
        """ В блоке try/except мы будем запускать генераторы и будем наполнять словари нужными нам парами """
        try:
            task = tasks.pop(0) # Получаем первое задание(первый элемент)

            reason, sock = next(task) # Распаковываем кортеж

            """ Cоздаем ключ socket для read и write """
            if reason == 'read': 
                to_read[sock] = task # <- это генератор 
            if reason == 'write': 
                to_write[sock] = task
        
        except StopIteration:
            logger.info('Done!')
        

tasks.append(server()) # В список tasks попадает генератор 
event_loop()