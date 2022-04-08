import socket # Сокет - это пара domain:port ('localhost:5000')
from requests import request
from loguru import logger


logger.add('debug_original_py.log', format='{time} {level} {message}', level = 'DEBUG')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Обслуживает запросы клиента 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
""" Устанавливаем таймаут 1 секунду, что бы использовать повторно один и тот же порт """ 
server_socket.bind(('localhost', 5000))
server_socket.listen() # Слушает входящие подключения 
logger.debug('RUN SERVER')


while True:
    logger.info('Waiting for user!')
    client_socket, addr = server_socket.accept()
    logger.info('Connection from', addr) 
    """ Принимает входящее подключения, читает данные из входящего буфера,
    если есть подключение, то он возращает кортеж и возвращает клиентский сокет и адресс """

    while True: 
        logger.info('There is a connection from the user!')
        # Дожидаемся от клиента сообщения  
        request = client_socket.recv(4096) # Принимаем от клиента сообщения
        logger.debug('Got data!')
        
        """ В цикле прерываем соединение, если ничего не пришло, или пишем соотвествующий текст , если нам что-то пришло """
        if not request:
            break
        else:
            response = 'Hellow maaan\n'.encode()
            client_socket.send(response)


    client_socket.close()
