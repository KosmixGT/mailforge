from fastapi import APIRouter, HTTPException, status, Depends
from app.application.dto.smtp import EmailDTO
from app.application.services.smtp_service import SMTPService

router = APIRouter(tags=["send_mailing"])


@router.post("/send_email")
async def send_email(email_data: EmailDTO, smtp_service: SMTPService = Depends()):
    success = await smtp_service.send_email(email_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email",
        )
    return {"message": "E-mail рассылка успешно отправлена"}
