from typing import Any, Dict, List, Optional

from src.database import Database
from src.interfaces.user_repository import AbstractUserRepository
from src.models.user import User


class UserRepository(AbstractUserRepository):
    def __init__(self, database: Database, collection: str = "users") -> None:
        self._db: Database = database
        self._collection: str = collection

    # TODO
    # Доделать методы класса:
    # - get_all
    # - get_filtered
    # - find_by_id
    # - find_by_username
    # - add
    # - update
    # - delete
