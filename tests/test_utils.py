"""
Тесты для вспомогательных функций.
"""

import unittest
from passgen.utils import validate_length, hash_password, verify_password


class TestUtils(unittest.TestCase):
    """Тесты для модуля utils."""

    def test_validate_length_valid(self):
        """Тестирует валидацию корректной длины."""
        self.assertTrue(validate_length(8))
        self.assertTrue(validate_length(12))
        self.assertTrue(validate_length(100))

    def test_validate_length_too_short(self):
        """Тестирует валидацию слишком короткой длины."""
        with self.assertRaises(ValueError) as context:
            validate_length(3)
        self.assertIn("не менее 4 символов", str(context.exception))

    def test_validate_length_too_long(self):
        """Тестирует валидацию слишком длинной длины."""
        with self.assertRaises(ValueError) as context:
            validate_length(101)
        self.assertIn("не должна превышать 100", str(context.exception))

    def test_validate_length_edge_cases(self):
        """Тестирует граничные случаи длины."""
        # Минимальная допустимая длина
        self.assertTrue(validate_length(4))

        # Максимальная допустимая длина
        self.assertTrue(validate_length(100))

    def test_hash_password(self):
        """Тестирует хэширование пароля."""
        password = "test_password_123"
        hashed = hash_password(password)

        # Проверяем что хэш не равен исходному паролю
        self.assertNotEqual(hashed, password)

        # Проверяем формат хэша (соль$хэш)
        self.assertIn('$', hashed)
        parts = hashed.split('$')
        self.assertEqual(len(parts), 2)

        # Проверяем что соль и хэш не пустые
        self.assertTrue(len(parts[0]) > 0)  # соль
        self.assertTrue(len(parts[1]) > 0)  # хэш

    def test_hash_password_different_results(self):
        """Тестирует что одинаковые пароли дают разные хэши."""
        password = "same_password"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)

        # Из-за использования соли хэши должны быть разными
        self.assertNotEqual(hashed1, hashed2)

    def test_verify_password_correct(self):
        """Тестирует проверку правильного пароля."""
        password = "test_password_123"
        hashed = hash_password(password)

        self.assertTrue(verify_password(password, hashed))

    def test_verify_password_incorrect(self):
        """Тестирует проверку неправильного пароля."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)

        self.assertFalse(verify_password(wrong_password, hashed))

    def test_verify_password_invalid_hash(self):
        """Тестирует проверку с некорректным хэшем."""
        password = "test_password_123"

        # Некорректный формат хэша
        self.assertFalse(verify_password(password, "invalid_hash_format"))
        self.assertFalse(verify_password(password, "no_delimiter"))
        self.assertFalse(verify_password(password, "only_salt$"))
        self.assertFalse(verify_password(password, "$only_hash"))

        # Пустой хэш
        self.assertFalse(verify_password(password, ""))
        self.assertFalse(verify_password(password, None))

    def test_verify_password_empty_password(self):
        """Тестирует проверку пустого пароля."""
        password = ""
        hashed = hash_password(password)

        self.assertTrue(verify_password(password, hashed))

        # Проверка пустого пароля с неправильным хэшем
        self.assertFalse(verify_password(password, "invalid$hash"))

    def test_verify_password_special_characters(self):
        """Тестирует проверку пароля со специальными символами."""
        special_passwords = [
            "p@ssw0rd!",
            "пароль123",
            "🔑emoji🔒",
            " space password ",
            "very_long_password_1234567890!@#$%^&*()"
        ]

        for password in special_passwords:
            with self.subTest(password=password):
                hashed = hash_password(password)
                self.assertTrue(verify_password(password, hashed))
                self.assertFalse(verify_password(password + "wrong", hashed))


if __name__ == '__main__':
    unittest.main()
