Документация Password Generator
===============================

.. toctree::
   :maxdepth: 2
   :caption: Содержание:

   installation
   usage
   modules

Введение
--------

Password Generator - это утилита командной строки для генерации и безопасного хранения паролей.

Основные возможности:

- Генерация безопасных паролей с настраиваемыми параметрами
- Безопасное хранение паролей с использованием хэширования
- Поиск и управление сохраненными паролями
- Удобный интерфейс командной строки
- Работа с PostgreSQL в качестве базы данных

Быстрый старт
-------------

.. code-block:: bash

   # Установка зависимостей
   pip install -r requirements.txt

   # Генерация пароля
   python main.py generate --length 16

   # Генерация и сохранение
   python main.py generate --length 12 --save --service gmail --username user@example.com

   # Поиск паролей
   python main.py find --service gmail

Индексы и таблицы
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`