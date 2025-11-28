"""
Пакет для генерации и управления паролями.

Модули:
    generator - Генерация паролей
    storage - Работа с базой данных
    utils - Вспомогательные функции
    commands - Обработчики команд CLI
"""

from .generator import PasswordGenerator
from .storage import PasswordStorage
from .utils import hash_password, verify_password, validate_length
from .commands import (
    handle_generate,
    handle_find,
    handle_list,
    handle_verify,
    handle_delete
)

__all__ = [
    'PasswordGenerator',
    'PasswordStorage',
    'hash_password',
    'verify_password',
    'validate_length',
    'handle_generate',
    'handle_find',
    'handle_list',
    'handle_verify',
    'handle_delete'
]
