from dataclasses import dataclass
from typing import Optional


@dataclass
class Recipient:
    id: Optional[int]
    mailing_id: int
    address_id: int
    delivery_status_id: Optional[int]
    history_id: int

    def validate(self) -> bool:
        return bool(self.mailing_id and self.address_id and self.history_id)

    def is_delivered(self) -> bool:
        return self.delivery_status_id == 1
