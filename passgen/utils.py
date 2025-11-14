import hashlib
import base64


def validate_length(length):
    """
    Проверка корректности длины пароля
    """
    if not isinstance(length, int) or length < 4:
        raise ValueError("Длина пароля должна быть целым числом не менее 4")
    if length > 100:
        raise ValueError("Длина пароля не должна превышать 100 символов")
    return True


def hash_password(password):
    """
    Хэширование пароля для безопасного хранения
    """
    try:
        # Создаем соль и хэшируем пароль
        salt = base64.b64encode(bytes(str(hash(password)), 'utf-8')[:16]).decode('utf-8')
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # Количество итераций
        )
        return f"{salt}${base64.b64encode(hashed).decode('utf-8')}"
    except Exception as e:
        raise Exception(f"Ошибка при хэшировании пароля: {str(e)}")
