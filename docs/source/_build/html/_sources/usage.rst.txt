Использование
=============

Базовое использование
---------------------

Генерация пароля
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Простая генерация
   python main.py generate --length 16

   # Пароль с определенными параметрами
   python main.py generate --length 16 --special --digits --uppercase

   # Пароль только из букв
   python main.py generate --length 12 --no-digits --no-special

   # Сохранение пароля
   python main.py generate --length 12 --save --service gmail --username user@example.com

Поиск паролей
~~~~~~~~~~~~~

.. code-block:: bash

   # Поиск по сервису
   python main.py find --service gmail

   # Поиск по пользователю
   python main.py find --username user@example.com

   # Просмотр всех паролей
   python main.py list

Примеры использования
---------------------

Пример 1: Генерация пароля для почты
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py generate --length 16 --special --digits --uppercase --save --service gmail --username user@gmail.com --description "Основная почта"

Пример 2: Генерация простого PIN-кода
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py generate --length 4 --no-uppercase --no-special --save --service bank --username card123 --description "PIN для банковской карты"