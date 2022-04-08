# Тестовый проект 
#### Программы написаны на языке програмирования ***`Python3.10`***, для того что бы научиться применять синхронный и асинхронный код. Проект содержит в себе ***` семь Python`*** файлов и сторонюю бибилиотеку [***`loguru`***](https://github.com/Delgan/loguru) для удобного логирования и демонстрации умениия пользоваться этой библиотекой, а так же текстовый документ с зависимостями.

# Описание проекта
#### Первые файл [***original.py***](asynchronous_py/../original.py), [***1_select.py***](asynchronous_py/../1_select.py) и [***2_selectors.py***](asynchronous_py/../2_selectors.py) - это классические синхронные программы на сокетах и селекторах, которые обрабатывают подключения по очереди, т.е, не могут работать с двумя и более соединениями. Они были написаны для того, что бы сначала разобраться в основах.
#### В файлe [***3_generator.py***](asynchronous_py/../3_generators.py) уже асинхронный код, который написан с использованием генераторов.
#### В файле [***one_synchronous.py***](asynchronous_py/../one_synchronous.py) и [***two_async.py***](asynchronous_py/../two_async.py) содержиться одинаковая программа. Один её вариант написан с применением синхронного кода, а другой вариант с применением асинхронного.Она рандомно загружает 10 файлов с котиками, с [***сайта***](https://loremflickr.com).Программа написанна с целью доказать то, что ассинхронный код работает быстрее чем синхронный, потому-что асинхронный код позволяет выполнить блок кода без остановки всего потока.
