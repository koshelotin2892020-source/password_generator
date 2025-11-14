import random as rnd
import string
from .utils import validate_length


class PasswordGenerator:
    """
    Генератор безопасных паролей.

    Attributes:
        char_sets (dict): Словарь с наборами символов для паролей
    """

    def __init__(self):
        """Инициализация генератора паролей."""
        self.char_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'special': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }

    def generate_password(self, length=12, use_uppercase=True, use_digits=True, use_special=True):
        """
        Генерация пароля с заданными параметрами.

        Args:
            length (int): Длина пароля (по умолчанию 12)
            use_uppercase (bool): Использовать заглавные буквы (по умолчанию True)
            use_digits (bool): Использовать цифры (по умолчанию True)
            use_special (bool): Использовать специальные символы (по умолчанию True)

        Returns:
            str: Сгенерированный пароль

        Raises:
            ValueError: Если не выбран ни один тип символов
            Exception: При ошибках генерации

        Example:
            >>> generator = PasswordGenerator()
            >>> password = generator.generate_password(length=16, use_special=True)
            >>> len(password)
            16
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
                raise ValueError("Должен быть выбран хотя бы 1 тип символов")

            # Генерируем пароль
            password = ''.join(rnd.choice(characters) for _ in range(length))

            # Проверяем, что пароль содержит выбранные типы символов
            # (функция проверки надежности пароля)
            if use_uppercase and not any(c in self.char_sets['uppercase']
                                         for c in password):
                password = self._ensure_character_type(
                    password, self.char_sets['uppercase']
                    )
            if use_digits and not any(c in self.char_sets['digits']
                                      for c in password):
                password = self._ensure_character_type(
                    password, self.char_sets['digits']
                    )
            if use_special and not any(c in self.char_sets['special']
                                       for c in password):
                password = self._ensure_character_type(
                    password, self.char_sets['special']
                    )

            return password

        except Exception as e:
            raise Exception(f"Ошибка при генерации пароля: {str(e)}")

    def _ensure_character_type(self, password, char_set):
        """
        Гарантирует, что пароль содержит хотя бы
        один символ из указанного набора
        """
        password_list = list(password)
        # Заменяем случайный символ на символ из нужного набора
        index = rnd.randint(0, len(password_list) - 1)
        password_list[index] = rnd.choice(char_set)
        return ''.join(password_list)
