"""
Тесты для команд CLI.
"""

import unittest
from unittest.mock import patch, MagicMock
from passgen.commands import (
    handle_generate,
    handle_find,
    handle_list,
    handle_verify,
    handle_delete
)


class TestCommands(unittest.TestCase):
    """Тесты для команд CLI."""

    def setUp(self):
        """Настройка перед каждым тестом."""
        self.mock_args = MagicMock()

    @patch('passgen.commands.PasswordGenerator')
    @patch('passgen.commands.print')
    def test_handle_generate_basic(self, mock_print, mock_generator):
        """Тестирует базовую генерацию пароля."""
        # Настраиваем моки
        mock_gen_instance = mock_generator.return_value
        mock_gen_instance.generate_password.return_value = "test_password_123"

        # Настраиваем аргументы
        self.mock_args.length = 12
        self.mock_args.uppercase = True
        self.mock_args.digits = True
        self.mock_args.special = True
        self.mock_args.save = False
        self.mock_args.service = None
        self.mock_args.username = None
        self.mock_args.description = ""

        # Вызываем функцию
        handle_generate(self.mock_args)

        # Проверяем вызовы
        mock_generator.assert_called_once()
        mock_gen_instance.generate_password.assert_called_once_with(
            length=12, use_uppercase=True, use_digits=True, use_special=True
        )
        mock_print.assert_called_with("Сгенерирован пароль: test_password_123")

    @patch('passgen.commands.PasswordGenerator')
    @patch('passgen.commands.PasswordStorage')
    @patch('passgen.commands.print')
    def test_handle_generate_with_save(self,
                                       mock_print,
                                       mock_storage,
                                       mock_generator
                                       ):
        """Тестирует генерацию с сохранением."""
        # Настраиваем моки
        mock_gen_instance = mock_generator.return_value
        mock_gen_instance.generate_password.return_value = "test_password_123"

        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.save_password.return_value = 1

        # Настраиваем аргументы
        self.mock_args.save = True
        self.mock_args.service = "test_service"
        self.mock_args.username = "test_user"
        self.mock_args.description = "test description"

        # Вызываем функцию
        handle_generate(self.mock_args)

        # Проверяем сохранение
        mock_storage_instance.save_password.assert_called_once_with(
            "test_service",
            "test_user",
            "test_password_123",
            "test description"
        )
        mock_print.assert_any_call("Пароль сохранен в базу данных (ID: 1)")

    @patch('passgen.commands.PasswordStorage')
    @patch('passgen.commands.print')
    def test_handle_find_with_results(self, mock_print, mock_storage):
        """Тестирует поиск с результатами."""
        # Настраиваем моки
        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.find_passwords.return_value = [
            {
                'service': 'gmail',
                'username': 'user1',
                'description': 'test description'
            }
        ]

        # Настраиваем аргументы
        self.mock_args.service = "gmail"
        self.mock_args.username = None

        # Вызываем функцию
        handle_find(self.mock_args)

        # Проверяем вывод
        mock_print.assert_any_call("Найдено записей: 1")
        mock_print.assert_any_call("1. Сервис: gmail")
        mock_print.assert_any_call("   Пользователь: user1")
        mock_print.assert_any_call("   Описание: test description")

    @patch('passgen.commands.PasswordStorage')
    @patch('passgen.commands.print')
    def test_handle_find_no_results(self, mock_print, mock_storage):
        """Тестирует поиск без результатов."""
        # Настраиваем моки
        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.find_passwords.return_value = []

        # Вызываем функцию
        handle_find(self.mock_args)

        # Проверяем вывод
        mock_print.assert_called_with("Пароли не найдены")

    @patch('passgen.commands.handle_find')
    def test_handle_list(self, mock_handle_find):
        """Тестирует команду list."""
        # Вызываем функцию
        handle_list(self.mock_args)

        # Проверяем что вызывается handle_find с правильными аргументами
        mock_handle_find.assert_called_once()

    @patch('passgen.commands.PasswordStorage')
    @patch('passgen.commands.print')
    def test_handle_verify_correct(self, mock_print, mock_storage):
        """Тестирует проверку правильного пароля."""
        # Настраиваем моки
        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.verify_password.return_value = True

        # Настраиваем аргументы
        self.mock_args.service = "gmail"
        self.mock_args.username = "user1"
        self.mock_args.password = "correct_password"

        # Вызываем функцию
        handle_verify(self.mock_args)

        # Проверяем вывод
        mock_print.assert_called_with("Пароль верный")

    @patch('passgen.commands.PasswordStorage')
    @patch('passgen.commands.print')
    def test_handle_verify_incorrect(self, mock_print, mock_storage):
        """Тестирует проверку неправильного пароля."""
        # Настраиваем моки
        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.verify_password.return_value = False

        # Настраиваем аргументы
        self.mock_args.service = "gmail"
        self.mock_args.username = "user1"
        self.mock_args.password = "wrong_password"

        # Вызываем функцию
        handle_verify(self.mock_args)

        # Проверяем вывод
        mock_print.assert_called_with("Пароль неверный или запись не найдена")

    @patch('passgen.commands.PasswordStorage')
    @patch('passgen.commands.print')
    def test_handle_delete_success(self, mock_print, mock_storage):
        """Тестирует успешное удаление."""
        # Настраиваем моки
        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.delete_password.return_value = True

        # Настраиваем аргументы
        self.mock_args.service = "gmail"
        self.mock_args.username = "user1"

        # Вызываем функцию
        handle_delete(self.mock_args)

        # Проверяем вывод
        mock_print.assert_called_with("Пароль для gmail/user1 удален")

    @patch('passgen.commands.PasswordStorage')
    @patch('passgen.commands.print')
    def test_handle_delete_not_found(self, mock_print, mock_storage):
        """Тестирует удаление несуществующего пароля."""
        # Настраиваем моки
        mock_storage_instance = mock_storage.return_value
        mock_storage_instance.delete_password.return_value = False

        # Настраиваем аргументы
        self.mock_args.service = "gmail"
        self.mock_args.username = "user1"

        # Вызываем функцию
        handle_delete(self.mock_args)

        # Проверяем вывод
        mock_print.assert_called_with("Пароль для gmail/user1 не найден")


if __name__ == '__main__':
    unittest.main()
