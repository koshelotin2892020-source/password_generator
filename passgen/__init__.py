"""
Пакет для генерации и управления паролями.

Модули:
    generator - Генерация паролей
    storage - Хранение паролей
    utils - Вспомогательные функции
    commands - Обработчики команд CLI
"""

from .generator import PasswordGenerator
from .storage import PasswordStorage
from .utils import validate_length, hash_password, verify_password
from .commands import handle_generate, handle_find, handle_list

__version__ = '1.0.0'
__author__ = 'Александр'
__all__ = [
    'PasswordGenerator',
    'PasswordStorage',
    'validate_length',
    'hash_password',
    'verify_password',
    'handle_generate',
    'handle_find',
    'handle_list'
]
