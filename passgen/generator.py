import random
import string
from .utils import validate_length


class PasswordGenerator:
    def __init__(self):
        self.char_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'special': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
    
    def generate_password(self, length=12, use_uppercase=True, use_digits=True, use_special=True):
        """
        Генерация пароля с заданными параметрами
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
            
            # Проверяем, что пароль содержит выбранные типы символов
            if use_uppercase and not any(c in self.char_sets['uppercase'] for c in password):
                password = self._ensure_character_type(password, self.char_sets['uppercase'])
            if use_digits and not any(c in self.char_sets['digits'] for c in password):
                password = self._ensure_character_type(password, self.char_sets['digits'])
            if use_special and not any(c in self.char_sets['special'] for c in password):
                password = self._ensure_character_type(password, self.char_sets['special'])
            
            return password
            
        except Exception as e:
            raise Exception(f"Ошибка при генерации пароля: {str(e)}")
    
    def _ensure_character_type(self, password, char_set):
        """
        Гарантирует, что пароль содержит хотя бы один символ из указанного набора
        """
        password_list = list(password)
        # Заменяем случайный символ на символ из нужного набора
        index = random.randint(0, len(password_list) - 1)
        password_list[index] = random.choice(char_set)
        return ''.join(password_list)