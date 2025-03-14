from app.application.services.smtp_service import SMTPService
from app.application.services.telegram_service import TelegramService
from app.application.dto.smtp import EmailDTO
from app.application.dto.telegram import TelegramDTO

class DeliveryService:
    def __init__(self, smtp_service: SMTPService, telegram_service: TelegramService):
        self.smtp_service = smtp_service
        self.telegram_service = telegram_service

    async def send_mailing(self, mailing_data: dict):
        mailing_type = mailing_data.get('type')
        
        if mailing_type == "email":
            email_dto = EmailDTO(**mailing_data['email_data'])
            await self.smtp_service.send_email(email_dto)
        elif mailing_type == 'telegram':
            telegram_data = TelegramDTO(
                bot_token="your_token",  # Get from config
                chat_ids=["@chat_id_example"],   # Get from config
                subject=mailing_data['data']['title'],
                body=mailing_data['data']['message']
            )
            await self.telegram_service.send_message(telegram_data)
