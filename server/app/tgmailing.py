from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import requests

router = APIRouter(tags=['send_mailing'])

# Модель данных для получения информации о рассылке в Telegram
class TelegramData(BaseModel):
    chat_ids: List[str]  # Список идентификаторов чатов
    subject: str  # Тема письма
    body: str  # Текст сообщения
    bot_token: str # Токен бота

# Обработчик для отправки сообщения в чат-каналы Telegram
@router.post("/send_telegram")
async def send_telegram(telegram_data: TelegramData):
    try:
        for chat_id in telegram_data.chat_ids:
            # Формируем URL для отправки сообщения в чат
            url = f"https://api.telegram.org/bot{telegram_data.bot_token}/sendMessage"
            
            # Формируем текст сообщения для отправки в Telegram
            message = f"{telegram_data.subject}\n\n{telegram_data.body}"
            # Параметры запроса
            params = {
                "chat_id": chat_id,
                "text": message
            }
            
            # Отправляем запрос
            response = requests.post(url, params=params)
            
            # Проверяем успешность запроса
            if not response.ok:
                raise HTTPException(status_code=response.status_code, detail="Ошибка отправления рассылки в Telegram")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Возвращаем ответ клиенту
    return {"message": "Рассылка в Telegram успешно отправлена"}
