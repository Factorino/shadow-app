from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_filtered(self, is_active: bool) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> Optional[User]:
        raise NotImplementedError
