from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass(slots=True, kw_only=True)
class User:
    username: str
    password: str
    is_active: bool = True
    id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
