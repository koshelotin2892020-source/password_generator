#!/usr/bin/env python3
"""
Генератор безопасных паролей CLI
"""

import argparse
import sys
from passgen.commands import handle_generate, handle_find, handle_list


def main():
    parser = argparse.ArgumentParser(
        description='Генератор безопасных паролей',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py generate --length 16 --special --digits --uppercase
  python main.py generate --length 12 --save --service gmail --username user@example.com
  python main.py find --service gmail
  python main.py list
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Парсер для команды generate
    generate_parser = subparsers.add_parser('generate', help='Генерация нового пароля')
    generate_parser.add_argument('--length', type=int, default=12, 
                               help='Длина пароля (по умолчанию: 12)')
    generate_parser.add_argument('--uppercase', action='store_true', default=True,
                               help='Использовать заглавные буквы (по умолчанию: True)')
    generate_parser.add_argument('--digits', action='store_true', default=True,
                               help='Использовать цифры (по умолчанию: True)')
    generate_parser.add_argument('--special', action='store_true', default=True,
                               help='Использовать специальные символы (по умолчанию: True)')
    generate_parser.add_argument('--save', action='store_true',
                               help='Сохранить пароль в файл')
    generate_parser.add_argument('--service', type=str,
                               help='Название сервиса для сохранения')
    generate_parser.add_argument('--username', type=str,
                               help='Имя пользователя для сохранения')
    generate_parser.add_argument('--description', type=str, default='',
                               help='Описание для сохранения')

    # Парсер для команды find
    find_parser = subparsers.add_parser('find', help='Поиск сохраненных паролей')
    find_parser.add_argument('--service', type=str,
                           help='Фильтр по названию сервиса')
    find_parser.add_argument('--username', type=str,
                           help='Фильтр по имени пользователя')

    # Парсер для команды list
    list_parser = subparsers.add_parser('list', help='Показать все сохраненные пароли')

    # Обработка аргументов
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
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
