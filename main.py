#!/usr/bin/env python3
"""
Главный модуль CLI для генератора паролей.

Этот модуль предоставляет интерфейс командной строки для управления паролями.
Использует argparse для обработки аргументов и делегирует выполнение 
в модуль commands.

Примеры использования:
    python main.py generate --length 16
    python main.py generate --save --service gmail --username user@example.com
    python main.py find --service gmail
    python main.py list
    python main.py verify --service gmail --username user --password "pass123"
    python main.py delete --service gmail --username user

Доступные команды:
    generate  - Генерация нового пароля
    find      - Поиск сохраненных паролей
    list      - Показать все пароли
    verify    - Проверить пароль
    delete    - Удалить пароль
"""

import argparse
import sys
from passgen.commands import (
    handle_generate,
    handle_find,
    handle_list,
    handle_verify,
    handle_delete
)


def main():
    """Основная функция для обработки команд CLI.

    Настраивает парсер аргументов и вызывает соответствующие обработчики
    из модуля commands.

    Raises:
        SystemExit: При завершении программы или ошибках.
    """
    parser = argparse.ArgumentParser(
        description='Генератор безопасных паролей с PostgreSQL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py generate --length 16 --no-special --no-digits --no-uppercase
  python main.py generate --length 12 --save --service gmail --username user
  python main.py find --service gmail
  python main.py list
  python main.py verify --service gmail --username user --password "my_pass"
  python main.py delete --service gmail --username user
        """
    )

    subparsers = parser.add_subparsers(dest='command',
                                       help='Доступные команды'
                                       )

    # Команда generate
    generate_parser = subparsers.add_parser('generate',
                                            help='Сгенерировать новый пароль'
                                            )
    generate_parser.add_argument('--length',
                                 type=int,
                                 default=12,
                                 help='Длина пароля (по умолчанию: 12)'
                                 )
    generate_parser.add_argument('--no-uppercase',
                                 dest='uppercase',
                                 action='store_false',
                                 help='Не использовать заглавные буквы'
                                 )
    generate_parser.add_argument('--no-digits',
                                 dest='digits',
                                 action='store_false',
                                 help='Не использовать цифры'
                                 )
    generate_parser.add_argument('--no-special',
                                 dest='special',
                                 action='store_false',
                                 help='Не использовать специальные символы'
                                 )
    generate_parser.add_argument('--save',
                                 action='store_true',
                                 help='Сохранить пароль в базу данных'
                                 )
    generate_parser.add_argument('--service',
                                 type=str,
                                 help='Название сервиса для сохранения'
                                 )
    generate_parser.add_argument('--username',
                                 type=str,
                                 help='Имя пользователя для сохранения'
                                 )
    generate_parser.add_argument('--description',
                                 type=str,
                                 default='',
                                 help='Описание для сохранения'
                                 )
    generate_parser.set_defaults(uppercase=True,
                                 digits=True,
                                 special=True
                                 )

    # Команда find
    find_parser = subparsers.add_parser('find',
                                        help='Найти сохраненные пароли'
                                        )
    find_parser.add_argument('--service',
                             type=str,
                             help='Фильтр по названию сервиса'
                             )
    find_parser.add_argument('--username',
                             type=str,
                             help='Фильтр по имени пользователя'
                             )

    # Команда list
    subparsers.add_parser('list',
                          help='Показать все сохраненные пароли'
                          )

    # Команда verify
    verify_parser = subparsers.add_parser('verify', help='Проверить пароль')
    verify_parser.add_argument('--service',
                               type=str,
                               required=True,
                               help='Название сервиса'
                               )
    verify_parser.add_argument('--username',
                               type=str,
                               required=True,
                               help='Имя пользователя'
                               )
    verify_parser.add_argument('--password',
                               type=str,
                               required=True,
                               help='Пароль для проверки'
                               )

    # Команда delete
    delete_parser = subparsers.add_parser('delete',
                                          help='Удалить пароль'
                                          )
    delete_parser.add_argument('--service',
                               type=str,
                               required=True,
                               help='Название сервиса'
                               )
    delete_parser.add_argument('--username',
                               type=str,
                               required=True,
                               help='Имя пользователя'
                               )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'generate':
            handle_generate(args)
        elif args.command == 'find':
            handle_find(args)
        elif args.command == 'list':
            handle_list(args)
        elif args.command == 'verify':
            handle_verify(args)
        elif args.command == 'delete':
            handle_delete(args)

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
