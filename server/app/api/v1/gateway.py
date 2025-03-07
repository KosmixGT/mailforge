from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any

from app.infrastructure.services.auth_service import AuthService
from app.infrastructure.services.mailing_service import MailingService
from app.infrastructure.services.delivery_service import DeliveryService

router = APIRouter()

# Сервисы
auth_service = AuthService()
mailing_service = MailingService()
delivery_service = DeliveryService()

# Auth routes
@router.post("/user/jwt/create/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.login(form_data.username, form_data.password)

# Mailing routes
@router.get("/mailings/")
async def get_mailings():
    return await mailing_service.get_mailings()

@router.post("/mailings/create")
async def create_mailing(data: Dict[str, Any]):
    return await mailing_service.create_mailing(data)

# Delivery routes
@router.post("/smtp/send/{mailing_id}")
async def send_smtp(mailing_id: int, data: Dict[str, Any]):
    return await delivery_service.send_smtp(mailing_id, data)

@router.post("/telegram/send/{mailing_id}")
async def send_telegram(mailing_id: int, data: Dict[str, Any]):
    return await delivery_service.send_telegram(mailing_id, data)
