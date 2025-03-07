from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from mailforge_shared.core.config.database import Base
from app.domain.models.recipient import Recipient as DomainRecipient


class RecipientModel(Base):
    __tablename__ = "recipients"

    recipientid = Column(Integer, primary_key=True)
    mailingid = Column(
        ForeignKey("mailings.mailingid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    addressid = Column(
        ForeignKey("addresses.addressid", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    # deliverystatusid = Column(
    #     ForeignKey(
    #         "deliverystatuses.deliverystatusid", ondelete="SET NULL", onupdate="CASCADE"
    #     )
    # )
    deliverystatusid = Column(Integer)  # Просто храним ID без ForeignKey
    # historyid = Column(
    #     ForeignKey("mailinghistory.historyid", ondelete="RESTRICT", onupdate="CASCADE"),
    #     nullable=False,
    # )
    historyid = Column(Integer)

    address = relationship("AddressModel")   
    mailing = relationship("MailingModel")

    def to_domain(self) -> DomainRecipient:
        return DomainRecipient(
            id=self.recipientid,
            mailing_id=self.mailingid,
            address_id=self.addressid,
            delivery_status_id=self.deliverystatusid,
            history_id=self.historyid,
        )

    @staticmethod
    def from_domain(recipient: DomainRecipient) -> "RecipientModel":
        return RecipientModel(
            recipientid=recipient.id,
            mailingid=recipient.mailing_id,
            addressid=recipient.address_id,
            deliverystatusid=recipient.delivery_status_id,
            historyid=recipient.history_id,
        )
