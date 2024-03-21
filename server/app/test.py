from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Модель данных для получения информации о письме от клиента
class EmailData:
    def __init__(self, recipient_emails: List[str], subject: str, body: str, smtp_host: str, smtp_port: int, smtp_username: str, smtp_password: str):
        self.recipient_emails = recipient_emails
        self.subject = subject
        self.body = body
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

def send_email(email_data: EmailData):
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
    
    print("Email sent successfully")

def main():
    # Получаем данные о письме от пользователя
    recipient_emails = "kostya.meckhonoshin@mail.ru"
    subject = "Test email"
    body = "Test email body"
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "kostya.vtanke@gmail.com"
    smtp_password = "oyjg lxme imup gayx"
    
    # Создаем объект EmailData
    email_data = EmailData(
        recipient_emails=recipient_emails,
        subject=subject,
        body=body,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_username=smtp_username,
        smtp_password=smtp_password
    )
    
    # Отправляем письмо
    send_email(email_data)

if __name__ == "__main__":
    main()
