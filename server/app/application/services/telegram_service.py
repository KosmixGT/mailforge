import requests
from fastapi import HTTPException, status
from app.application.dto.telegram import TelegramDTO


class TelegramService:
    async def send_message(self, telegram_data: TelegramDTO) -> bool:
        try:
            for chat_id in telegram_data.chat_ids:
                url = (
                    f"https://api.telegram.org/bot{telegram_data.bot_token}/sendMessage"
                )
                message = f"{telegram_data.subject}\n\n{telegram_data.body}"

                params = {"chat_id": chat_id, "text": message}

                response = requests.post(url, params=params)
                if not response.ok:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Ошибка отправления рассылки в Telegram",
                    )
            return True

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
