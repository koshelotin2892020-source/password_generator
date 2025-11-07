from .generator import PasswordGenerator
from .storage import PasswordStorage


def handle_generate(args):
    """
    Обработчик команды генерации пароля
    """
    try:
        generator = PasswordGenerator()
        password = generator.generate_password(
            length=args.length,
            use_uppercase=args.uppercase,
            use_digits=args.digits,
            use_special=args.special
        )

        print(f"Сгенерированный пароль: {password}")

        # Сохранение в файл, если указано
        if args.save:
            storage = PasswordStorage()
            service = args.service or "unknown_service"
            username = args.username or "unknown_user"
            description = args.description or ""

            record_id = storage.save_password(service, username, password, description)
            print(f"Пароль сохранен с ID: {record_id}")

    except Exception as e:
        print(f"Ошибка: {str(e)}")


def handle_find(args):
    """
    Обработчик команды поиска паролей
    """
    try:
        storage = PasswordStorage()
        results = storage.find_password(
            service=args.service,
            username=args.username
        )

        if not results:
            print("Пароли не найдены")
            return

        print(f"Найдено записей: {len(results)}")
        for i, result in enumerate(results, 1):
            print(f"{i}. Сервис: {result['service']}")
            print(f"   Пользователь: {result['username']}")
            print(f"   Описание: {result['description']}")
            print()

    except Exception as e:
        print(f"Ошибка: {str(e)}")


def handle_list(args):
    """
    Обработчик команды списка всех паролей
    """
    try:
        storage = PasswordStorage()
        results = storage.list_all()

        if not results:
            print("Нет сохраненных паролей")
            return

        print(f"Всего сохраненных паролей: {len(results)}")
        for i, result in enumerate(results, 1):
            print(f"{i}. Сервис: {result['service']}")
            print(f"   Пользователь: {result['username']}")
            print(f"   Описание: {result['description']}")
            print()

    except Exception as e:
        print(f"Ошибка: {str(e)}")
