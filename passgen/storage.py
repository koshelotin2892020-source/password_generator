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
            
            # Пытаемся вставить новую запись
            cur.execute("""
                INSERT INTO passwords (service, username, password_hash, description)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (service, username, hashed_password, description))
            
            record_id = cur.fetchone()[0]
            conn.commit()
            return record_id
            
        except psycopg2.IntegrityError:
            # Запись уже существует - обновляем существующую
            conn.rollback()
            return self._update_password(service, username, password, description)
        except Exception as e:
            conn.rollback()
            raise Exception(f"Ошибка при сохранении пароля: {str(e)}")
        finally:
            cur.close()
            conn.close()
    
    def _update_password(self, service, username, password, description=""):
        """Обновляет существующий пароль.
        
        Args:
            service (str): Название сервиса.
            username (str): Имя пользователя.
            password (str): Новый пароль.
            description (str): Новое описание.
            
        Returns:
            int: ID обновленной записи.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            hashed_password = hash_password(password)
            
            cur.execute("""
                UPDATE passwords 
                SET password_hash = %s, description = %s
                WHERE service = %s AND username = %s
                RETURNING id
            """, (hashed_password, description, service, username))
            
            result = cur.fetchone()
            conn.commit()
            
            if result:
                return result[0]
            else:
                raise Exception("Запись не найдена для обновления")
                
        except Exception as e:
            conn.rollback()
            raise Exception(f"Ошибка при обновлении пароля: {str(e)}")
        finally:
            cur.close()
            conn.close()
    
    def save_or_update_password(self, service, username, password, description=""):
        """Сохраняет или обновляет пароль с явным указанием действия.
        
        Args:
            service (str): Название сервиса.
            username (str): Имя пользователя.
            password (str): Пароль.
            description (str): Описание.
            
        Returns:
            tuple: (action, record_id) где action: 'created' или 'updated'
        """
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Сначала проверяем существует ли запись
            cur.execute("""
                SELECT id FROM passwords 
                WHERE service = %s AND username = %s
            """, (service, username))
            
            existing_record = cur.fetchone()
            hashed_password = hash_password(password)
            
            if existing_record:
                # Обновляем существующую запись
                cur.execute("""
                    UPDATE passwords 
                    SET password_hash = %s, description = %s
                    WHERE service = %s AND username = %s
                    RETURNING id
                """, (hashed_password, description, service, username))
                action = 'updated'
            else:
                # Создаем новую запись
                cur.execute("""
                    INSERT INTO passwords (service, username, password_hash, description)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (service, username, hashed_password, description))
                action = 'created'
            
            record_id = cur.fetchone()[0]
            conn.commit()
            return action, record_id
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Ошибка при сохранении пароля: {str(e)}")
        finally:
            cur.close()
            conn.close()
    
    def find_passwords(self, service=None, username=None):
        """Ищет пароли по сервису и/или имени пользователя."""
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            query = "SELECT id, service, username, description FROM passwords WHERE 1=1"
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
