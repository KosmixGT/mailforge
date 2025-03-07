from typing import Dict, Any
import httpx
from fastapi import HTTPException

class DeliveryService:
    def __init__(self, base_url: str = "http://delivery:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
    
    async def send_smtp(self, mailing_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Отправка через SMTP"""
        try:
            response = await self.client.post(
                f"/api/smtp/send/{mailing_id}",
                json=data
            )
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def send_telegram(self, mailing_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Отправка через Telegram"""
        try:
            response = await self.client.post(
                f"/api/telegram/send/{mailing_id}",
                json=data
            )
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.client.aclose()
