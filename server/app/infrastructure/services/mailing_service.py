from typing import Dict, Any, List
import httpx
from fastapi import HTTPException

class MailingService:
    def __init__(self, base_url: str = "http://mailing:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
    
    async def get_mailings(self) -> List[Dict[str, Any]]:
        """Получение списка рассылок"""
        try:
            response = await self.client.get("/api/v1/mailings/")
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def create_mailing(self, mailing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание новой рассылки"""
        try:
            response = await self.client.post(
                "/api/mailings/create",
                json=mailing_data
            )
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_mailing(self, mailing_id: int) -> Dict[str, Any]:
        """Получение рассылки по ID"""
        try:
            response = await self.client.get(f"/api/mailings/{mailing_id}")
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.client.aclose()
