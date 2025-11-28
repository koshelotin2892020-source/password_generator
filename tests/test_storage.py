"""
Тесты для хранилища паролей.
"""

import unittest
from passgen.storage import PasswordStorage
from passgen.utils import verify_password


class TestPasswordStorage(unittest.TestCase):
    """Тесты для хранилища паролей."""

    def setUp(self):
        """Настройка перед каждым тестом."""
        self.storage = PasswordStorage()
        self.test_service = "test_service"
        self.test_username = "test_user"
        self.test_password = "test_password_123"
        self.test_description = "test description"

    def tearDown(self):
        """Очистка после каждого теста."""
        # Удаляем тестовые данные
        try:
            self.storage.delete_password(self.test_service, self.test_username)
        except Exception:
            pass

    def test_save_password(self):
        """Тестирует сохранение пароля."""
        record_id = self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password,
            self.test_description
        )

        self.assertIsInstance(record_id, int)
        self.assertGreater(record_id, 0)

    def test_save_password_duplicate(self):
        """Тестирует попытку сохранения дубликата."""
        # Первое сохранение
        self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password
        )

        # Попытка сохранить дубликат
        with self.assertRaises(Exception) as context:
            self.storage.save_password(
                self.test_service,
                self.test_username,
                "another_password"
            )

        self.assertIn("уже существует", str(context.exception))

    def test_find_passwords_by_service(self):
        """Тестирует поиск по сервису."""
        # Сохраняем тестовые данные
        self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password,
            self.test_description
        )

        # Ищем по сервису
        results = self.storage.find_passwords(service=self.test_service)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['service'], self.test_service)
        self.assertEqual(results[0]['username'], self.test_username)
        self.assertEqual(results[0]['description'], self.test_description)

    def test_find_passwords_by_username(self):
        """Тестирует поиск по имени пользователя."""
        # Сохраняем тестовые данные
        self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password
        )

        # Ищем по имени пользователя
        results = self.storage.find_passwords(username=self.test_username)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['username'], self.test_username)

    def test_find_passwords_no_results(self):
        """Тестирует поиск когда нет результатов."""
        results = self.storage.find_passwords(service="non_existent_service")
        self.assertEqual(len(results), 0)

    def test_verify_password_correct(self):
        """Тестирует проверку правильного пароля."""
        self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password
        )

        is_valid = self.storage.verify_password(
            self.test_service,
            self.test_username,
            self.test_password
        )

        self.assertTrue(is_valid)

    def test_verify_password_incorrect(self):
        """Тестирует проверку неправильного пароля."""
        self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password
        )

        is_valid = self.storage.verify_password(
            self.test_service,
            self.test_username,
            "wrong_password"
        )

        self.assertFalse(is_valid)

    def test_verify_password_nonexistent(self):
        """Тестирует проверку пароля для несуществующей записи."""
        is_valid = self.storage.verify_password(
            "non_existent_service",
            "non_existent_user",
            self.test_password
        )

        self.assertFalse(is_valid)

    def test_delete_password(self):
        """Тестирует удаление пароля."""
        # Сначала сохраняем
        self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password
        )

        # Затем удаляем
        success = self.storage.delete_password(self.test_service,
                                               self.test_username
                                               )
        self.assertTrue(success)

        # Проверяем что запись удалена
        results = self.storage.find_passwords(service=self.test_service)
        self.assertEqual(len(results), 0)

    def test_delete_nonexistent_password(self):
        """Тестирует удаление несуществующего пароля."""
        success = self.storage.delete_password("non_existent", "non_existent")
        self.assertFalse(success)

    def test_list_all(self):
        """Тестирует получение списка всех паролей."""
        # Сохраняем несколько записей
        test_data = [
            ("service1", "user1", "pass1"),
            ("service2", "user2", "pass2"),
            ("service3", "user3", "pass3"),
        ]

        for service, username, password in test_data:
            self.storage.save_password(service, username, password)

        # Получаем все записи
        results = self.storage.list_all()

        # Должно быть как минимум наши тестовые записи
        self.assertGreaterEqual(len(results), len(test_data))

        # Очистка
        for service, username, _ in test_data:
            self.storage.delete_password(service, username)

    def test_password_is_hashed_in_storage(self):
        """Тестирует что пароль хранится в хэшированном виде."""
        # Сохраняем пароль
        self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password
        )

        # Проверяем что пароль можно верифицировать
        is_valid = self.storage.verify_password(
            self.test_service,
            self.test_username,
            self.test_password
        )
        self.assertTrue(is_valid)

        # Проверяем что неправильный пароль не проходит
        is_valid_wrong = self.storage.verify_password(
            self.test_service,
            self.test_username,
            "wrong_password"
        )
        self.assertFalse(is_valid_wrong)

    def test_password_hash_verification(self):
        """Тестирует прямую проверку хэширования через utils."""
        # Сохраняем пароль
        self.storage.save_password(
            self.test_service,
            self.test_username,
            self.test_password
        )

        # Получаем хэш из базы данных (для внутренней проверки)
        import psycopg2
        import os
        from dotenv import load_dotenv

        load_dotenv()

        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            dbname=os.getenv('DB_NAME', 'password_manager'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )

        cur = conn.cursor()
        cur.execute(
            '''
            SELECT password_hash FROM passwords
            WHERE service = %s AND username = %s
            ''',
            (self.test_service, self.test_username)
        )

        result = cur.fetchone()
        self.assertIsNotNone(result)

        stored_hash = result[0]

        # Проверяем что хэш работает с функцией verify_password
        self.assertTrue(verify_password(self.test_password, stored_hash))
        self.assertFalse(verify_password("wrong_password", stored_hash))

        cur.close()
        conn.close()


if __name__ == '__main__':
    unittest.main()
