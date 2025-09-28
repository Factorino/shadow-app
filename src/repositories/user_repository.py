from typing import Any, Dict, List, Optional

from src.database import Database
from src.interfaces.user_repository import AbstractUserRepository
from src.models.user import User


class UserRepository(AbstractUserRepository):
    def __init__(self, database: Database, collection: str = "users") -> None:
        self._db: Database = database
        self._collection: str = collection

    def get_all(self) -> List[User]:
        users_data: List[Dict[str, Any]] = self._db.get_all(self._collection)
        return [User(**user_data) for user_data in users_data]

    def get_filtered(self, is_active: bool) -> List[User]:
        users_data: List[Dict[str, Any]] = self._db.get_all(self._collection)
        filtered_users: List[User] = [
            User(**user_data)
            for user_data in users_data
            if user_data.get("is_active") == is_active
        ]
        return filtered_users

    def find_by_id(self, user_id: int) -> Optional[User]:
        user_data: Optional[Dict[str, Any]] = self._db.find_by_id(
            self._collection, user_id
        )
        if user_data is None:
            return None
        return User(**user_data)

    def find_by_username(self, username: str) -> Optional[User]:
        user_data: Optional[Dict[str, Any]] = self._db.find_by_field(
            self._collection, "username", username
        )
        if user_data is None:
            return None
        return User(**user_data)

    def add(self, user: User) -> User:
        user_data: Dict[str, Any] = user.to_dict()
        created_user_data: Dict[str, Any] = self._db.add(self._collection, user_data)
        return User(**created_user_data)

    def update(self, user: User) -> Optional[User]:
        if user.id is None:
            raise ValueError("Cannot update user without ID")

        user_data: Dict[str, Any] = user.to_dict()
        updated_user_data: Optional[Dict[str, Any]] = self._db.update(
            self._collection, user.id, user_data
        )
        if updated_user_data is None:
            return None
        return User(**updated_user_data)

    def delete(self, user_id: int) -> Optional[User]:
        user_data: Optional[Dict[str, Any]] = self._db.delete(self._collection, user_id)
        if user_data is None:
            return None
        return User(**user_data)
