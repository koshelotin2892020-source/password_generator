Модули
======

Пакет passgen
-------------

.. automodule:: passgen
   :members:
   :undoc-members:
   :show-inheritance:

Модуль generator
----------------

Модуль для генерации безопасных паролей.

.. automodule:: passgen.generator
   :members:
   :undoc-members:
   :show-inheritance:

Модуль storage
--------------

Модуль для работы с хранилищем паролей в PostgreSQL.

.. automodule:: passgen.storage
   :members:
   :undoc-members:
   :show-inheritance:

Модуль utils
------------

Вспомогательные функции для работы с паролями.

.. automodule:: passgen.utils
   :members:
   :undoc-members:
   :show-inheritance:

Модуль database
---------------

Модуль для работы с базой данных PostgreSQL.

.. automodule:: passgen.database
   :members:
   :undoc-members:
   :show-inheritance:

Модуль commands
---------------

Модуль с обработчиками команд для CLI.

.. automodule:: passgen.commands
   :members:
   :undoc-members:
   :show-inheritance:

Основной модуль (CLI)
---------------------

Главный скрипт командной строки. Обрабатывает аргументы и делегирует выполнение командам.

**Функции:**
    - main() - Основная точка входа в программу

**Аргументы командной строки:**
    - generate - Генерация паролей
    - find - Поиск паролей  
    - list - Список всех паролей
    - verify - Проверка паролей
    - delete - Удаление паролей

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance: