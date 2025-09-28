import json
import os
from typing import Any, Dict, List, Optional

from src.config import config


class Database:
    def __init__(self) -> None:
        self.filename: str = config.DATA_FILENAME
        self._ensure_file_exists()

    def get_all(self, collection: str) -> List[Dict[str, Any]]:
        data: Dict[str, Any] = self._read_data()
        if collection not in data:
            raise ValueError(f"Collection not found: {collection}")
        collection_dict: Dict[str, Any] = data.get(collection, {})
        return list(collection_dict.values())

    def find_by_field(
        self, collection: str, field_name: str, field_value: Any
    ) -> Optional[Dict[str, Any]]:
        items_dict: Dict[int, Dict[str, Any]] = self._get_all_dict(collection)
        for item in items_dict.values():
            if item.get(field_name) == field_value:
                return item
        return None

    def find_by_id(self, collection: str, item_id: int) -> Optional[Dict[str, Any]]:
        items_dict: Dict[int, Dict[str, Any]] = self._get_all_dict(collection)
        return items_dict.get(item_id)

    def add(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        data_dict: Dict[str, Any] = self._read_data()

        if collection not in data_dict:
            raise ValueError(f"Collection not found: {collection}")

        # Получаем следующий ID из счетчика
        next_id: int = data_dict["counters"].get(collection, 0) + 1

        # Устанавливаем ID для данных
        data_with_id: Dict[str, Any] = data.copy()
        data_with_id["id"] = next_id

        # Добавляем в коллекцию
        data_dict[collection][next_id] = data_with_id

        # Обновляем счетчик
        data_dict["counters"][collection] = next_id

        # Сохраняем изменения
        self._write_data(data_dict)
        return data_with_id

    def update(
        self, collection: str, item_id: int, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        data_dict: Dict[str, Any] = self._read_data()

        if collection not in data_dict:
            raise ValueError(f"Collection not found: {collection}")

        # Проверяем существование записи
        if item_id not in data_dict[collection]:
            return None

        # Сохраняем ID и обновляем остальные поля
        updated_data: Dict[str, Any] = data.copy()
        updated_data["id"] = item_id
        data_dict[collection][item_id] = updated_data

        # Сохраняем изменения
        self._write_data(data_dict)
        return updated_data

    def delete(self, collection: str, item_id: int) -> Optional[Dict[str, Any]]:
        data_dict: Dict[str, Any] = self._read_data()

        if collection not in data_dict:
            raise ValueError(f"Collection not found: {collection}")

        # Проверяем существование записи
        if item_id not in data_dict[collection]:
            return None

        deleted_data: Dict[str, Any] = data_dict[collection][item_id]
        del data_dict[collection][item_id]

        # Сохраняем изменения
        self._write_data(data_dict)
        return deleted_data

    def _get_all_dict(self, collection: str) -> Dict[int, Dict[str, Any]]:
        data: Dict[str, Any] = self._read_data()
        if collection not in data:
            raise ValueError(f"Collection not found: {collection}")
        return data.get(collection, {})

    def _read_data(self) -> Dict[str, Any]:
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self._ensure_file_exists()
            return self._read_data()

    def _write_data(self, data: Dict[str, Any]) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def _ensure_file_exists(self) -> None:
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(
                    config.INITIAL_DATA_TEMPLATE, file, indent=4, ensure_ascii=False
                )
