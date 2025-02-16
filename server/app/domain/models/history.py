from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MailingHistory:
    id: Optional[int]
    mailing_id: int
    sent_time: datetime
    delivery_status_id: int

    def validate(self) -> bool:
        return bool(self.mailing_id and self.sent_time and self.delivery_status_id)
