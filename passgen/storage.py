"""
Модуль для работы с хранилищем паролей в PostgreSQL.

Содержит класс PasswordStorage для операций с базой данных.
"""

import psycopg2
# from psycopg2 import IntegrityError
from .database import get_db_connection
from .utils import hash_password, verify_password


class PasswordStorage:
    """Класс для управления паролями в базе данных."""

    def save_password(self, service, username, password, description=""):
        """Сохраняет пароль в базу данных в хэшированном виде.

        Args:
            service (str): Название сервиса.
            username (str): Имя пользователя.
            password (str): Пароль для сохранения.
            description (str): Описание пароля. По умолчанию пустая строка.

        Returns:
            int: ID сохраненной записи или None если запись уже существует.

        Raises:
            Exception: При ошибках сохранения.
        """
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            hashed_password = hash_password(password)

            cur.execute("""
                INSERT INTO passwords
                (service, username, password_hash, description)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (service, username, hashed_password, description))

            record_id = cur.fetchone()[0]
            conn.commit()
            return record_id

        except psycopg2.IntegrityError:
            conn.rollback()
            raise Exception(f'''Запись для {service}/{username} уже существует.
                            Используйте delete.''')
        except Exception as e:
            conn.rollback()
            raise Exception(f"Ошибка при сохранении: {str(e)}")
        finally:
            cur.close()
            conn.close()

    def find_passwords(self, service=None, username=None):
        """Ищет пароли по сервису и/или имени пользователя."""
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            query = '''
            SELECT id, service, username, description FROM passwords WHERE 1=1
            '''
            params = []

            if service:
                query += " AND service ILIKE %s"
                params.append(f"%{service}%")

            if username:
                query += " AND username ILIKE %s"
                params.append(f"%{username}%")

            query += " ORDER BY service, username"

            cur.execute(query, params)
            results = []

            for row in cur.fetchall():
                results.append({
                    'id': row[0],
                    'service': row[1],
                    'username': row[2],
                    'description': row[3] or ''
                })

            return results

        except Exception as e:
            raise Exception(f"Ошибка при поиске паролей: {str(e)}")
        finally:
            cur.close()
            conn.close()

    def verify_password(self, service, username, password):
        """Проверяет пароль для указанного сервиса и пользователя."""
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT password_hash FROM passwords
                WHERE service = %s AND username = %s
            """, (service, username))

            result = cur.fetchone()
            if not result:
                return False

            stored_hash = result[0]
            return verify_password(password, stored_hash)

        except Exception as e:
            raise Exception(f"Ошибка при проверке пароля: {str(e)}")
        finally:
            cur.close()
            conn.close()

    def delete_password(self, service, username):
        """Удаляет пароль для указанного сервиса и пользователя."""
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                DELETE FROM passwords
                WHERE service = %s AND username = %s
            """, (service, username))

            deleted_count = cur.rowcount
            conn.commit()

            return deleted_count > 0

        except Exception as e:
            conn.rollback()
            raise Exception(f"Ошибка при удалении пароля: {str(e)}")
        finally:
            cur.close()
            conn.close()

    def list_all(self):
        """Возвращает список всех сохраненных паролей."""
        return self.find_passwords()
