import selectors # Функция мониторинга над файломи, сокетами, и над всем что имеет файловый дискриптор 
import socket


selector = selectors.DefaultSelector() # Создаем дефолтный селектор


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()


    """ Метод регистрации нужных нам сокетов """
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)
    """ Приминаем 3 аргумента (1: Файловый объект, 2: Событие которое нас интересует, 3: Любые связанные данные например id ) """


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept() # Что бы клиент продвинулся дальше нужно создать входящее подключение 
    """ Подключаемся к сокету через nc, или telnet, как душе угодно """
    
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)
    """ Для мониторинга клиентского сокета """

    print('Connection from', addr)
        

def send_message(client_socket): # Функция отправки и получения сообщения от пользователя, она будет принимать клиентский сокет 

    request = client_socket.recv(4096)

    """ Условия для прерывания данного цыкла """
    if request:
        response = 'Hellow man!!!!!\n'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket) 
        """" Прежде чем закрыть сокет, нужно его снять с регистрации и передаем туда тот объект, который раньше регистрировали  """
        client_socket.close()


def event_loop(): # Функиция которая определяет вызов нашего кода 

    """ Метод селект работает с любыми файловыми объектами, у которых  есть метод 
    .fileno() - этот метод возвращает файловый дискриптор 
    (т.е номер файла, который ассоциируется с конкретным файлом в системе ) """
    
    while True:
        
        events = selector.select() # Метод select возвращает кортеж (key, events)
        # SelectorKey, fileobj, events, data
        
        """ Распаковывае список кортежей "events" """
        for key, _ in events:
            callback = key.data # Получаем обратно свою функцию, функции сохранены в атребуте "data=send_message"
            callback(key.fileobj) # Fileobj - это сам сокет 


if __name__ == '__main__':
    server()
    event_loop()    