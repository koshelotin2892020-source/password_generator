"""
Тесты для генератора паролей.
"""

import unittest
import string
from passgen.generator import PasswordGenerator


class TestPasswordGenerator(unittest.TestCase):
    """Тесты для генератора паролей."""

    def setUp(self):
        """Настройка перед каждым тестом."""
        self.generator = PasswordGenerator()

    def test_generate_password_default_length(self):
        """Тестирует генерацию пароля с длиной по умолчанию."""
        password = self.generator.generate_password()
        self.assertEqual(len(password), 12)

    def test_generate_password_custom_length(self):
        """Тестирует генерацию пароля с пользовательской длиной."""
        for length in [8, 16, 20]:
            with self.subTest(length=length):
                password = self.generator.generate_password(length=length)
                self.assertEqual(len(password), length)

    def test_generate_password_only_lowercase(self):
        """Тестирует генерацию пароля только из строчных букв."""
        password = self.generator.generate_password(
            length=10,
            use_uppercase=False,
            use_digits=False,
            use_special=False
        )

        # Проверяем что все символы - строчные буквы
        for char in password:
            self.assertIn(char, string.ascii_lowercase)

    def test_generate_password_with_uppercase(self):
        """Тестирует генерацию пароля с заглавными буквами."""
        password = self.generator.generate_password(
            length=15,
            use_uppercase=True,
            use_digits=False,
            use_special=False
        )

        # Проверяем что есть хотя бы одна заглавная буква
        has_uppercase = any(char in string.ascii_uppercase
                            for char in password)
        self.assertTrue(has_uppercase)

    def test_generate_password_with_digits(self):
        """Тестирует генерацию пароля с цифрами."""
        password = self.generator.generate_password(
            length=15,
            use_uppercase=False,
            use_digits=True,
            use_special=False
        )

        # Проверяем что есть хотя бы одна цифра
        has_digits = any(char in string.digits for char in password)
        self.assertTrue(has_digits)

    def test_generate_password_with_special(self):
        """Тестирует генерацию пароля со специальными символами."""
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        password = self.generator.generate_password(
            length=15,
            use_uppercase=False,
            use_digits=False,
            use_special=True
        )

        # Проверяем что есть хотя бы один специальный символ
        has_special = any(char in special_chars for char in password)
        self.assertTrue(has_special)

    def test_generate_password_all_characters(self):
        """Тестирует генерацию пароля со всеми типами символов."""
        password = self.generator.generate_password(
            length=20,
            use_uppercase=True,
            use_digits=True,
            use_special=True
        )

        # Проверяем наличие разных типов символов
        has_lowercase = any(char in string.ascii_lowercase
                            for char in password)
        has_uppercase = any(char in string.ascii_uppercase
                            for char in password)
        has_digits = any(char in string.digits
                         for char in password)
        has_special = any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?'
                          for char in password)

        self.assertTrue(has_lowercase)
        self.assertTrue(has_uppercase)
        self.assertTrue(has_digits)
        self.assertTrue(has_special)

    def test_generate_password_different_calls(self):
        """Тестирует что разные вызовы дают разные результаты."""
        password1 = self.generator.generate_password(length=12)
        password2 = self.generator.generate_password(length=12)

        # Пароли должны быть разными (из-за случайности)
        self.assertNotEqual(password1, password2)

    def test_ensure_character_types_adds_missing_uppercase(self):
        """Тестирует добавление заглавных букв если их нет."""
        # Пароль без заглавных букв
        original_password = "abc123!@#"
        result = self.generator._ensure_character_types(
            password=original_password,
            use_uppercase=True,
            use_digits=False,  # Цифры уже есть
            use_special=False  # Спецсимволы уже есть
        )

        # Проверяем что добавилась хотя бы одна заглавная буква
        has_uppercase = any(c in string.ascii_uppercase for c in result)
        self.assertTrue(has_uppercase, "Должна быть добавлена заглавная буква")

        # Длина не должна измениться
        self.assertEqual(len(result), len(original_password))

    def test_ensure_character_types_adds_missing_digits(self):
        """Тестирует добавление цифр если их нет."""
        # Пароль без цифр
        original_password = "ABCdef!@#"
        result = self.generator._ensure_character_types(
            password=original_password,
            use_uppercase=False,  # Заглавные уже есть
            use_digits=True,
            use_special=False     # Спецсимволы уже есть
        )

        # Проверяем что добавилась хотя бы одна цифра
        has_digits = any(c in string.digits for c in result)
        self.assertTrue(has_digits, "Должна быть добавлена цифра")
        self.assertEqual(len(result), len(original_password))

    def test_ensure_character_types_adds_missing_special(self):
        """Тестирует добавление спецсимволов если их нет."""
        # Пароль без спецсимволов
        original_password = "ABCdef123"
        result = self.generator._ensure_character_types(
            password=original_password,
            use_uppercase=False,  # Заглавные уже есть
            use_digits=False,     # Цифры уже есть
            use_special=True
        )

        # Проверяем что добавился хотя бы один спецсимвол
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        has_special = any(c in special_chars for c in result)
        self.assertTrue(has_special, "Должен быть добавлен спецсимвол")
        self.assertEqual(len(result), len(original_password))

    def test_ensure_character_types_preserves_good_password(self):
        """Тестирует что хороший пароль не изменяется."""
        # Пароль уже содержит все типы символов
        good_password = "Abc123!@#"
        result = self.generator._ensure_character_types(
            password=good_password,
            use_uppercase=True,
            use_digits=True,
            use_special=True
        )

        # Пароль не должен измениться
        self.assertEqual(result, good_password)

    def test_ensure_character_types_adds_multiple_missing_types(self):
        """Тестирует добавление нескольких отсутствующих типов символов."""
        # Пароль только из строчных букв
        original_password = "abcdefghjk"
        result = self.generator._ensure_character_types(
            password=original_password,
            use_uppercase=True,
            use_digits=True,
            use_special=True
        )

        # Проверяем что добавились все недостающие типы
        has_uppercase = any(c in string.ascii_uppercase for c in result)
        has_digits = any(c in string.digits for c in result)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in result)

        self.assertTrue(has_uppercase, "Должны быть заглавные буквы")
        self.assertTrue(has_digits, "Должны быть цифры")
        self.assertTrue(has_special, "Должны быть спецсимволы")
        self.assertEqual(len(result), len(original_password))

    def test_ensure_character_types_disabled_types(self):
        """Тестирует что отключенные типы символов не добавляются."""
        # Пароль только из строчных букв
        original_password = "abcdefgh"
        result = self.generator._ensure_character_types(
            password=original_password,
            use_uppercase=False,  # Отключены
            use_digits=False,     # Отключены
            use_special=False     # Отключены
        )

        # Пароль не должен измениться
        self.assertEqual(result, original_password)

        # Проверяем что нет лишних символов
        has_only_lowercase = all(c in string.ascii_lowercase for c in result)
        self.assertTrue(has_only_lowercase)

    def test_ensure_character_types_edge_case_single_character(self):
        """Тестирует обработку пароля из одного символа."""
        original_password = "a"
        result = self.generator._ensure_character_types(
            password=original_password,
            use_uppercase=True,
            use_digits=True,
            use_special=True
        )

        # Должен остаться один символ, но теперь это может быть любой тип
        self.assertEqual(len(result), 1)
        self.assertIn(result[0],
                      string.ascii_lowercase +
                      string.ascii_uppercase +
                      string.digits +
                      '!@#$%^&*()_+-=[]{}|;:,.<>?'
                      )


if __name__ == '__main__':
    unittest.main()
