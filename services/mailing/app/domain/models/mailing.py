from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Mailing:
    id: Optional[int]
    title: str
    message_text: str
    user_id: int
    scheduled_time: datetime
    status_id: int

    def is_scheduled(self) -> bool:
        return self.scheduled_time > datetime.now()

    def is_draft(self) -> bool:
        return self.status_id == 1

    def can_be_edited(self) -> bool:
        return self.is_draft() or self.is_scheduled()

    def validate(self) -> bool:
        return bool(
            self.title and self.message_text and self.user_id and self.status_id
        )
