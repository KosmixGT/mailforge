import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException, status
from app.application.dto.smtp import EmailDTO


class SMTPService:
    async def send_email(self, email_data: EmailDTO) -> bool:
        try:
            with smtplib.SMTP(email_data.smtp_host, email_data.smtp_port) as server:
                server.starttls()
                try:
                    server.login(email_data.smtp_username, email_data.smtp_password)
                except smtplib.SMTPAuthenticationError:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Ошибка аутентификации SMTP:"
                        " неверное имя пользователя или пароль",
                    )

                message = MIMEMultipart()
                message["From"] = email_data.smtp_username
                message["To"] = ", ".join(email_data.recipient_emails)
                message["Subject"] = email_data.subject
                message.attach(MIMEText(email_data.body, "plain"))

                try:
                    server.sendmail(
                        email_data.smtp_username,
                        email_data.recipient_emails,
                        message.as_string(),
                    )
                except smtplib.SMTPException as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Ошибка SMTP: {str(e)}",
                    )

        except smtplib.SMTPConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Не удалось подключиться к SMTP серверу",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Произошла ошибка при отправке: {str(e)}",
            )

        return True
