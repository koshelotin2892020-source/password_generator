"""
Модуль для работы с базой данных PostgreSQL.

Содержит функции для подключения к БД и создания таблиц.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Создает подключение к PostgreSQL и гарантирует существование таблицы.

    Returns:
        psycopg2.connection: Объект подключения к базе данных.

    Raises:
        Exception: При ошибках подключения к БД.

    Example:
        >>> conn = get_db_connection()
        >>> conn.closed
        0
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            dbname=os.getenv('DB_NAME', 'password_generator'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )

        # Создаем таблицу если не существует
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id SERIAL PRIMARY KEY,
                service VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password_hash TEXT NOT NULL,
                description TEXT,
                UNIQUE(service, username)
            )
        """)
        conn.commit()
        cur.close()

        return conn
    except Exception as e:
        raise Exception(f"Ошибка подключения к базе данных: {str(e)}")
