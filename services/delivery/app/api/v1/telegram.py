from fastapi import APIRouter, Depends
from app.application.dto.telegram import TelegramDTO
from app.application.services.telegram_service import TelegramService

router = APIRouter(tags=["send_mailing"])


@router.post("/send_telegram")
async def send_telegram(
    telegram_data: TelegramDTO, telegram_service: TelegramService = Depends()
):
    await telegram_service.send_message(telegram_data)
    return {"message": "Рассылка в Telegram успешно отправлена"}
