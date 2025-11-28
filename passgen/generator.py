"""
Модуль для генерации безопасных паролей.

Содержит класс PasswordGenerator для создания паролей с различными параметрами.
"""

import random
import string
from .utils import validate_length


class PasswordGenerator:
    """Генератор безопасных паролей с настраиваемыми параметрами.

    Attributes:
        char_sets (dict): Словарь с наборами символов для паролей.
    """

    def __init__(self):
        """Инициализирует генератор с наборами символов."""
        self.char_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'special': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }

    def generate_password(self, length=12, use_uppercase=True, use_digits=True, use_special=True):
        """Генерирует пароль с заданными параметрами.

        Args:
            length (int): Длина пароля. По умолчанию 12.
            use_uppercase (bool): Использовать заглавные буквы. По умолчанию True.
            use_digits (bool): Использовать цифры. По умолчанию True.
            use_special (bool): Использовать специальные символы. По умолчанию True.

        Returns:
            str: Сгенерированный пароль.

        Raises:
            ValueError: Если не выбран ни один тип символов.
            Exception: При ошибках генерации.
            
        Example:
            >>> generator = PasswordGenerator()
            >>> password = generator.generate_password(length=8)
            >>> len(password)
            8
        """
        try:
            validate_length(length)
            
            # Базовый набор символов (всегда есть строчные буквы)
            characters = self.char_sets['lowercase']
            
            # Добавляем дополнительные наборы символов
            if use_uppercase:
                characters += self.char_sets['uppercase']
            if use_digits:
                characters += self.char_sets['digits']
            if use_special:
                characters += self.char_sets['special']
            
            # Проверяем, что есть хотя бы один набор символов
            if not characters:
                raise ValueError("Должен быть выбран хотя бы один тип символов")
            
            # Генерируем пароль
            password = ''.join(random.choice(characters) for _ in range(length))
            
            # Гарантируем, что пароль содержит выбранные типы символов
            password = self._ensure_character_types(
                password, use_uppercase, use_digits, use_special
            )
            
            return password
            
        except Exception as e:
            raise Exception(f"Ошибка при генерации пароля: {str(e)}")
    
    def _ensure_character_types(self, password, use_uppercase, use_digits, use_special):
        """Гарантирует, что пароль содержит все выбранные типы символов.
        
        Args:
            password (str): Исходный пароль.
            use_uppercase (bool): Нужны ли заглавные буквы.
            use_digits (bool): Нужны ли цифры.
            use_special (bool): Нужны ли спецсимволы.
            
        Returns:
            str: Пароль с гарантированными типами символов.
        """
        password_list = list(password)
        
        if use_uppercase and not any(c in self.char_sets['uppercase'] for c in password):
            index = random.randint(0, len(password_list) - 1)
            password_list[index] = random.choice(self.char_sets['uppercase'])
        
        if use_digits and not any(c in self.char_sets['digits'] for c in password):
            index = random.randint(0, len(password_list) - 1)
            password_list[index] = random.choice(self.char_sets['digits'])
        
        if use_special and not any(c in self.char_sets['special'] for c in password):
            index = random.randint(0, len(password_list) - 1)
            password_list[index] = random.choice(self.char_sets['special'])
        
        return ''.join(password_list)
