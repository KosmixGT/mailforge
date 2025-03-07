from pydantic import BaseModel
from typing import List


class EmailDTO(BaseModel):
    recipient_emails: List[str]
    subject: str
    body: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
