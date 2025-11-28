"""
Конфигурация для тестов.
"""

import os
import pytest
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройки тестовой базы данных
TEST_DB_NAME = "test_password_manager"


@pytest.fixture
def test_db_config():
    """Возвращает конфигурацию для тестовой базы данных."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'dbname': TEST_DB_NAME,
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', '')
    }
