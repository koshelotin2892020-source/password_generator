"""
Тесты для модуля базы данных.
"""

import unittest
import psycopg2
from passgen.database import get_db_connection


class TestDatabase(unittest.TestCase):
    """Тесты для модуля database."""

    def test_get_db_connection_success(self):
        """Тестирует успешное подключение к базе данных."""
        try:
            conn = get_db_connection()
            self.assertFalse(conn.closed)
            conn.close()
        except psycopg2.OperationalError as e:
            self.skipTest(f"Не удалось подключиться к БД: {e}")
        except Exception as e:
            self.fail(f"Неожиданная ошибка при подключении к БД: {e}")

    def test_table_creation(self):
        """Тестирует создание таблицы при подключении."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Проверяем что таблица существует
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_name = 'passwords'
            """)
            result = cur.fetchone()

            self.assertIsNotNone(result)
            self.assertEqual(result[0], 'passwords')

            # Проверяем структуру таблицы
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'passwords'
            """)
            columns = [row[0] for row in cur.fetchall()]

            expected_columns = ['id',
                                'service',
                                'username',
                                'password_hash',
                                'description'
                                ]
            for column in expected_columns:
                self.assertIn(column, columns)

            cur.close()
            conn.close()

        except psycopg2.OperationalError as e:
            self.skipTest(f"Не удалось подключиться к БД: {e}")
        except Exception as e:
            self.fail(f"Неожиданная ошибка при проверке таблицы: {e}")


if __name__ == '__main__':
    unittest.main()
