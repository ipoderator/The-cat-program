import socket
from select import select 
""" Системная функция которая нужна для мониторинга файловых объектов(сокетов) """

to_monitor = [] # Список для мониторинга

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Обслуживает запросы клиента 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
""" Устанавливаем таймаут 1 секунду, что бы использовать повторно один и тот же порт """ 
server_socket.bind(('localhost', 5000))
server_socket.listen() # Слушает входящие подключения 


def accept_connection(server_socket): # Принятие соединения
    client_socket, addr = server_socket.accept()
    """ Функция принимает входящее подключение, читает данные из входящего буфера,
    если есть подключение, то она возращает кортеж и возвращает клиентский сокет и адресс  """
    
    to_monitor.append(client_socket) # Добавляем в очередь для мониторинга новый элемент 


def send_message(client_socket: str) -> str: # Принимает клиентский сокет
    # Дожидаемся от клиента сообщения  
    request = client_socket.recv(4096) # Принимаем от клиента какое-то сообщение

    """ В цикле прерываем соединение, если ничего не пришло или пишем соотвествующий текст, если нам что-то пришло """
    if  request:
        response = 'Hellow maaan\n'.encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:

        ready_to_read, _, _ = select(to_monitor, [], []) # read, write, errors
        
        """ Есть список с сокетами (to_monitor), который нужно мониторить, когда они станут доступны для чтения - это превый список
        2 список - это список объектов готовыми для записи и 3 список - это ошибки 
        Функция (select) делает выборку на предмет готовы ли объекты для чтения, записи, или нет"""
        
        for sock in ready_to_read: # Обраабатываем объекты готовые для чтения в цикле 
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock) # Если сокет клиентский, передаем его в функцию send_message


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()