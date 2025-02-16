from app.domain.models.mailing import Mailing
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.mailing_status import MailingStatusModel


class MailingModel(Base):
    __tablename__ = "mailings"

    mailingid = Column(Integer, primary_key=True)
    userid = Column(ForeignKey("users.userid"), nullable=False)
    title = Column(String(255), nullable=False)
    messagetext = Column(Text, nullable=False)
    scheduledtime = Column(DateTime)
    statusid = Column(ForeignKey("mailingstatuses.statusid"), nullable=False)

    mailingstatus = relationship("MailingStatusModel")
    user = relationship("UserModel")

    def to_domain(self) -> "Mailing":
        from app.domain.models.mailing import Mailing

        return Mailing(
            id=self.mailingid,
            title=self.title,
            message_text=self.messagetext,
            user_id=self.userid,
            scheduled_time=self.scheduledtime,
            status_id=self.statusid,
        )

    @staticmethod
    def from_domain(mailing: "Mailing") -> "MailingModel":
        return MailingModel(
            mailingid=mailing.id,
            title=mailing.title,
            messagetext=mailing.message_text,
            userid=mailing.user_id,
            scheduledtime=mailing.scheduled_time,
            statusid=mailing.status_id,
        )
