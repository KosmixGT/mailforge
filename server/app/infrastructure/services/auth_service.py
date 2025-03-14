from typing import Dict, Any
import httpx
from fastapi import HTTPException


class AuthService:
    def __init__(self, base_url: str = "http://auth:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """Аутентификация пользователя"""
        try:
            response = await self.client.post(
                "/api/v1/auth/jwt/create",
                data={"username": username, "password": password},
            )
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Проверка токена"""
        try:
            response = await self.client.get(
                "/api/user/verify/", headers={"Authorization": f"Bearer {token}"}
            )
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.client.aclose()
