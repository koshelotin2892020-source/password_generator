"""
Модуль с обработчиками команд для CLI.

Содержит функции для обработки аргументов командной строки.
"""

from .generator import PasswordGenerator
from .storage import PasswordStorage


def handle_generate(args):
    """Обрабатывает команду генерации пароля.
    
    Args:
        args: Аргументы командной строки.
        
    Example:
        >>> args = type('Args', (), {
        ...     'length': 12, 'uppercase': True, 'digits': True,
        ...     'special': True, 'save': False, 'service': None,
        ...     'username': None, 'description': ''
        ... })()
        >>> handle_generate(args)  # Выведет сгенерированный пароль
    """
    try:
        generator = PasswordGenerator()
        password = generator.generate_password(
            length=args.length,
            use_uppercase=args.uppercase,
            use_digits=args.digits,
            use_special=args.special
        )
        
        print(f"🔑 Сгенерированный пароль: {password}")
        
        if args.save:
            storage = PasswordStorage()
            service = args.service or "unknown_service"
            username = args.username or "unknown_user"
            
            try:
                # Пытаемся сохранить новую запись
                record_id = storage.save_password(service, username, password, args.description)
                print(f"✅ Пароль сохранен в базу данных (ID: {record_id})")
            except Exception as e:
                if "уже существует" in str(e).lower():
                    # Предлагаем пользователю варианты
                    print(f"⚠️  Запись для {service}/{username} уже существует")
                    print("💡 Используйте другую пару service/username или удалите старую запись")
                else:
                    raise e
            
    except Exception as e:
        print(f"❌ Ошибка при генерации: {e}")


def handle_find(args):
    """Обрабатывает команду поиска паролей.
    
    Args:
        args: Аргументы командной строки.
        
    Example:
        >>> args = type('Args', (), {'service': 'gmail', 'username': None})()
        >>> handle_find(args)  # Выведет найденные пароли
    """
    try:
        storage = PasswordStorage()
        results = storage.find_passwords(args.service, args.username)
        
        if not results:
            print("📭 Пароли не найдены")
            return
        
        print(f"📋 Найдено записей: {len(results)}")
        for i, item in enumerate(results, 1):
            print(f"{i}. Сервис: {item['service']}")
            print(f"   Пользователь: {item['username']}")
            if item['description']:
                print(f"   Описание: {item['description']}")
            print()
            
    except Exception as e:
        print(f"❌ Ошибка при поиске: {e}")


def handle_list(args):
    """Обрабатывает команду показа всех паролей.
    
    Args:
        args: Аргументы командной строки (игнорируются).
        
    Example:
        >>> handle_list(None)  # Выведет все пароли
    """
    handle_find(type('Args', (), {'service': None, 'username': None})())


def handle_verify(args):
    """Обрабатывает команду проверки пароля.
    
    Args:
        args: Аргументы командной строки.
        
    Example:
        >>> args = type('Args', (), {
        ...     'service': 'gmail', 'username': 'user', 'password': 'pass123'
        ... })()
        >>> handle_verify(args)  # Проверит пароль
    """
    try:
        storage = PasswordStorage()
        is_valid = storage.verify_password(args.service, args.username, args.password)
        
        if is_valid:
            print("✅ Пароль верный")
        else:
            print("❌ Пароль неверный или запись не найдена")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке: {e}")


def handle_delete(args):
    """Обрабатывает команду удаления пароля.
    
    Args:
        args: Аргументы командной строки.
        
    Example:
        >>> args = type('Args', (), {'service': 'gmail', 'username': 'user'})()
        >>> handle_delete(args)  # Удалит пароль
    """
    try:
        storage = PasswordStorage()
        success = storage.delete_password(args.service, args.username)
        
        if success:
            print(f"✅ Пароль для {args.service}/{args.username} удален")
        else:
            print(f"❌ Пароль для {args.service}/{args.username} не найден")
            
    except Exception as e:
        print(f"❌ Ошибка при удалении: {e}")
