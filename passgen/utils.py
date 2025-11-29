"""
Вспомогательные функции для работы с паролями.

Содержит функции для хэширования, проверки паролей и валидации.
"""

import hashlib
import base64
import os


def validate_length(length):
    """Проверяет корректность длины пароля.

    Args:
        length (int): Длина пароля для проверки.

    Returns:
        bool: True если длина корректна.

    Raises:
        ValueError: Если длина меньше 4 или больше 100.

    Example:
        >>> validate_length(12)
        True
        >>> validate_length(3)
        ValueError: Длина пароля должна быть не менее 4 символов
    """
    if length < 4:
        raise ValueError("Длина пароля должна быть не менее 4 символов")
    if length > 100:
        raise ValueError("Длина пароля не должна превышать 100 символов")
    return True


def hash_password(password):
    """Хэширует пароль с использованием PBKDF2 и salt.

    Args:
        password (str): Пароль для хэширования.

    Returns:
        str: Хэшированный пароль в формате "salt$hash".

    Raises:
        Exception: При ошибках хэширования.
    """
    try:
        # Генерируем случайную соль
        salt = base64.b64encode(os.urandom(16)).decode('utf-8')

        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${base64.b64encode(hashed).decode('utf-8')}"
    except Exception as e:
        raise Exception(f"Ошибка при хэшировании пароля: {str(e)}")


def verify_password(password, hash_passw):
    """Проверяет пароль против хэша.

    Args:
        password (str): Пароль для проверки.
        hashed_password (str): Хэшированный пароль для сравнения.

    Returns:
        bool: True если пароль верный, иначе False.

    Example:
        >>> hashed = hash_password("test")
        >>> verify_password("test", hashed)
        True
        >>> verify_password("wrong", hashed)
        False
    """
    # Проверяем базовые условия перед split
    if (not hash_passw or not isinstance(hash_passw,
                                         str) or '$' not in hash_passw):
        return False
    try:
        parts = hash_passw.split('$')

        # Проверяем что есть обе части (соль и хэш)
        if len(parts) != 2:
            return False

        salt, stored_hash = parts

        # Проверяем что обе части не пустые
        if not salt or not stored_hash:
            return False

        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return base64.b64encode(new_hash).decode('utf-8') == stored_hash
    except (ValueError, TypeError, UnicodeDecodeError):
        return False
