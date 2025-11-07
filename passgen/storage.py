import json
import os
from .utils import hash_password, verify_password


class PasswordStorage:
    def __init__(self, filename='passwords.json'):
        self.filename = filename
        self._ensure_storage_file()

    def _ensure_storage_file(self):
        """
        Создает файл хранилища, если он не существует
        """
        try:
            if not os.path.exists(self.filename):
                with open(self.filename, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"Ошибка при создании файла хранилища: {str(e)}")

    def save_password(self, service, username, password, description=""):
        """
        Сохранение пароля в файл (в хэшированном виде)
        """
        try:
            # Читаем существующие данные
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Хэшируем пароль
            hashed_password = hash_password(password)

            # Сохраняем запись
            record_id = f"{service}_{username}"
            data[record_id] = {
                'service': service,
                'username': username,
                'password_hash': hashed_password,
                'description': description
            }

            # Записываем обратно
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return record_id

        except Exception as e:
            raise Exception(f"Ошибка при сохранении пароля: {str(e)}")

    def find_password(self, service=None, username=None):
        """
        Поиск паролей по сервису и/или имени пользователя
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            results = []
            for record_id, record in data.items():
                matches_service = service is None or service.lower() in record['service'].lower()
                matches_username = username is None or username.lower() in record['username'].lower()

                if matches_service and matches_username:
                    results.append({
                        'service': record['service'],
                        'username': record['username'],
                        'description': record['description']
                    })

            return results

        except Exception as e:
            raise Exception(f"Ошибка при поиске паролей: {str(e)}")

    def list_all(self):
        """
        Получение списка всех сохраненных паролей (без самих паролей)
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return [
                {
                    'service': record['service'],
                    'username': record['username'],
                    'description': record['description']
                }
                for record in data.values()
            ]
        except Exception as e:
            raise Exception(f"Ошибка при получении списка паролей: {str(e)}")
