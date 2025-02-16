from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    password: str
    role_id: int

    def validate(self) -> bool:
        return bool(self.name and self.email and self.password and self.role_id)

    def has_admin_rights(self) -> bool:
        return self.role_id == 1

    def can_manage_mailings(self) -> bool:
        return self.role_id in [1, 2]
