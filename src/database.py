import json
import os
from typing import Any, Dict, List, Optional

from src.config import config


class Database:
    def __init__(self) -> None:
        self.filename: str = config.DATA_FILENAME
        self._ensure_file_exists()

    def get_all(self, collection: str) -> List[Dict[str, Any]]:
        pass

    def find_by_field(
        self, collection: str, field_name: str, field_value: Any
    ) -> Optional[Dict[str, Any]]:
        pass

    def find_by_id(self, collection: str, item_id: int) -> Optional[Dict[str, Any]]:
        items_dict: Dict[int, Dict[str, Any]] = self._get_all_dict(collection)
        return items_dict.get(item_id)

    def add(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def update(
        self, collection: str, item_id: int, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        pass

    def delete(self, collection: str, item_id: int) -> Optional[Dict[str, Any]]:
        pass

    def _get_all_dict(self, collection: str) -> Dict[int, Dict[str, Any]]:
        pass

    def _read_data(self) -> Dict[str, Any]:
        pass

    def _write_data(self, data: Dict[str, Any]) -> None:
        pass

    def _ensure_file_exists(self) -> None:
        pass
