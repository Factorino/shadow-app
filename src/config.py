from typing import Any, Dict, Final


class Config:
    DATA_FILENAME: Final[str] = "data.json"

    INITIAL_DATA_TEMPLATE: Final[Dict[str, Any]] = {
        "users": {},
        "counters": {
            "users": 0,
        },
    }


config = Config()
