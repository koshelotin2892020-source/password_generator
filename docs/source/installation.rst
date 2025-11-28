Установка
=========

Системные требования
--------------------

- Python 3.7 или выше
- PostgreSQL 12 или выше
- pip (менеджер пакетов Python)

Установка зависимостей
----------------------

1. Клонируйте репозиторий:

   .. code-block:: bash

      git clone <repository-url>
      cd password_generator

2. Установите зависимости:

   .. code-block:: bash

      pip install -r requirements.txt

3. Настройте базу данных:

   Создайте файл ``.env`` в корне проекта со следующим содержимым:

   .. code-block:: ini

      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=password_manager
      DB_USER=postgres
      DB_PASSWORD=your_password

4. Создайте базу данных:

   .. code-block:: sql

      CREATE DATABASE password_manager;

Проверка установки
------------------

Запустите тестовую команду:

.. code-block:: bash

   python main.py generate --length 12

Если вы видите сгенерированный пароль - установка прошла успешно!

Запуск тестов
-------------

.. code-block:: bash

   # Все тесты
   python -m unittest

   # Конкретный тестовый модуль
   python -m unittest tests.test_generator

   # С подробным выводом
   python -m unittest tests.test_utils -v