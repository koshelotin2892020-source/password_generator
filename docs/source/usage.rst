Использование
=============

Обзор команд
------------

Программа предоставляет следующие команды:

- ``generate`` - Генерация пароля
- ``find`` - Поиск паролей
- ``list`` - Список всех паролей
- ``verify`` - Проверка пароля
- ``delete`` - Удаление пароля

Генерация паролей
-----------------

Базовая генерация:

.. code-block:: bash

   python main.py generate --length 16

Генерация с определенными параметрами:

.. code-block:: bash

   # Без специальных символов
   python main.py generate --length 12 --no-special

   # Только строчные буквы
   python main.py generate --length 8 --no-uppercase --no-digits --no-special

   # Только цифры
   python main.py generate --length 6 --no-uppercase --no-special

Сохранение в базу данных:

.. code-block:: bash

   python main.py generate --length 12 --save --service gmail --username user@example.com --description "Рабочая почта"

Поиск и управление
------------------

Поиск паролей:

.. code-block:: bash

   # Поиск по сервису
   python main.py find --service gmail

   # Поиск по пользователю
   python main.py find --username user@example.com

   # Комбинированный поиск
   python main.py find --service gmail --username user@example.com

Просмотр всех паролей:

.. code-block:: bash

   python main.py list

Проверка пароля
---------------

Команда ``verify`` позволяет проверить, соответствует ли введенный пароль сохраненному в базе данных.

Проверка правильного пароля:

.. code-block:: bash

   python main.py verify --service gmail --username user@example.com --password "correct_password"

Результат при правильном пароле:

.. code-block:: text

   Пароль верный

Проверка неправильного пароля:

.. code-block:: bash

   python main.py verify --service gmail --username user@example.com --password "wrong_password"

Результат при неправильном пароле:

.. code-block:: text

   Пароль неверный или запись не найдена

Проверка несуществующей записи:

.. code-block:: bash

   python main.py verify --service nonexistent --username unknown --password "any_password"

Результат:

.. code-block:: text

   Пароль неверный или запись не найдена

Удаление пароля:

.. code-block:: bash

   python main.py delete --service gmail --username user@example.com

Примеры использования
---------------------

Пример 1: Создание пароля для почты
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py generate --length 16 --special --digits --uppercase --save --service gmail --username user@gmail.com --description "Основная почта"

Пример 2: Создание PIN-кода
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python main.py generate --length 4 --no-uppercase --no-special --save --service bank --username card123 --description "PIN для банковской карты"

Пример 3: Проверка доступа к сервису
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Предположим, вы забыли какой пароль используете для определенного сервиса:

.. code-block:: bash

   # Сначала найдем все записи для сервиса
   python main.py find --service github

   # Результат:
   # 1. Сервис: github
   #    Пользователь: developer
   #    Описание: Рабочий аккаунт

   # Теперь проверим несколько паролей
   python main.py verify --service github --username developer --password "password123"
   # Пароль неверный или запись не найдена

   python main.py verify --service github --username developer --password "dev123456"
   # Пароль верный

Пример 4: Восстановление доступа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Если вы сменили пароль на сайте и хотите обновить его в менеджере:

.. code-block:: bash

   # 1. Проверим старый пароль (для уверенности)
   python main.py verify --service facebook --username myuser --password "old_password"
   # Пароль верный

   # 2. Удалим старую запись
   python main.py delete --service facebook --username myuser

   # 3. Создадим новую запись с новым паролем
   python main.py generate --length 16 --save --service facebook --username myuser --description "Обновленный пароль"