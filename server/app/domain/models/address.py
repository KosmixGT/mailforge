from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    id: Optional[int]
    type_id: int
    address: str

    def validate(self) -> bool:
        return bool(self.address and self.type_id)

    def is_email(self) -> bool:
        return self.type_id == 1

    def is_telegram(self) -> bool:
        return self.type_id == 2
