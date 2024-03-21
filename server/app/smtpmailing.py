from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

router = APIRouter(tags=['sending_email'])

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
    # Создаем объект SMTP-клиента
    with smtplib.SMTP(email_data.smtp_host, email_data.smtp_port) as server:
        # Подключаемся к серверу
        server.starttls()
        # Логинимся на сервере
        server.login(email_data.smtp_username, email_data.smtp_password)
        
        # Создаем сообщение
        message = MIMEMultipart()
        message['From'] = email_data.smtp_username
        message['To'] = ", ".join(email_data.recipient_emails)
        message['Subject'] = email_data.subject
        message.attach(MIMEText(email_data.body, 'plain'))
        
        # Отправляем сообщение
        server.sendmail(email_data.smtp_username, email_data.recipient_emails, message.as_string())
    
    # Возвращаем ответ клиенту
    return {"message": "Email sent successfully"}
