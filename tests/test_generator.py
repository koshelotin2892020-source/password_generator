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

    def test_generate_password_no_character_types(self):
        """Тестирует ошибку при отсутствии типов символов."""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_password(
                use_uppercase=False,
                use_digits=False,
                use_special=False
            )
        self.assertIn("хотя бы один тип символов", str(context.exception))

    def test_generate_password_unique(self):
        """Тестирует что пароли уникальны."""
        passwords = set()
        for _ in range(10):
            password = self.generator.generate_password(length=8)
            passwords.add(password)

        # Проверяем что все пароли уникальны
        self.assertEqual(len(passwords), 10)


if __name__ == '__main__':
    unittest.main()
