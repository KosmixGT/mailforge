from pydantic import BaseModel
from typing import List


class TelegramDTO(BaseModel):
    chat_ids: List[str]
    subject: str
    body: str
    bot_token: str
