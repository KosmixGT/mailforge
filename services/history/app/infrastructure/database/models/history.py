from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from mailforge_shared.core.config.database import Base
from app.domain.models.history import MailingHistory as DomainHistory


class MailingHistoryModel(Base):
    __tablename__ = "mailinghistory"

    historyid = Column(Integer, primary_key=True)
    mailingid: Mapped[int] = mapped_column(
        ForeignKey("mailings.mailingid"), nullable=False
    )
    senttime = Column(DateTime, nullable=False)
    deliverystatusid = Column(Integer)  # Просто храним ID статуса
    # deliverystatusid = Column(ForeignKey("deliverystatuses.deliverystatusid"))

    # deliverystatus = relationship("DeliveryStatusModel")
    mailing = relationship("MailingModel")

    def to_domain(self) -> DomainHistory:
        return DomainHistory(
            id=self.historyid,
            mailing_id=self.mailingid,
            sent_time=self.senttime,
            delivery_status_id=self.deliverystatusid,
        )

    @staticmethod
    def from_domain(history: DomainHistory) -> "MailingHistoryModel":
        return MailingHistoryModel(
            historyid=history.id,
            mailingid=history.mailing_id,
            senttime=history.sent_time,
            deliverystatusid=history.delivery_status_id,
        )
