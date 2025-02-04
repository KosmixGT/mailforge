from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

router = APIRouter(tags=['send_mailing'])

# Модель данных для получения информации о письме от клиента
class EmailData(BaseModel):
    recipient_emails: List[str]  # Список адресов получателей
    subject: str  # Тема письма
    body: str  # Текст сообщения
    smtp_host: str  # Хост SMTP-сервера
    smtp_port: int  # Порт SMTP-сервера
    smtp_username: str  # Имя пользователя SMTP
    smtp_password: str  # Пароль SMTP

# Обработчик для отправки электронного письма
@router.post("/send_email")
async def send_email(email_data: EmailData):
    try:
        with smtplib.SMTP(email_data.smtp_host, email_data.smtp_port) as server:
            server.starttls()
            server.login(email_data.smtp_username, email_data.smtp_password)
            
            message = MIMEMultipart()
            message['From'] = email_data.smtp_username
            message['To'] = ", ".join(email_data.recipient_emails)
            message['Subject'] = email_data.subject
            message.attach(MIMEText(email_data.body, 'plain'))
            
            server.sendmail(email_data.smtp_username, email_data.recipient_emails, message.as_string())
        
        return {"message": "E-mail рассылка успешно отправлена"}
        
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка аутентификации SMTP: неверное имя пользователя или пароль"
        )
    except smtplib.SMTPConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Не удалось подключиться к SMTP серверу"
        )
    except smtplib.SMTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка SMTP: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при отправке: {str(e)}"
        )
