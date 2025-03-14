from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from mailforge_shared.core.config.database import Base
from app.domain.models.address import Address as DomainAddress
from app.infrastructure.database.models.mailing_type import MailingTypeModel


class AddressModel(Base):
    __tablename__ = "addresses"

    addressid = Column(Integer, primary_key=True)
    typeid: Mapped[int] = mapped_column(
        ForeignKey("mailingtypes.typeid", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    address = Column(String(255), nullable=False, unique=True)

    mailingtype = relationship(MailingTypeModel)

    def to_domain(self) -> DomainAddress:
        return DomainAddress(
            id=self.addressid, type_id=self.typeid, address=self.address
        )

    @staticmethod
    def from_domain(address: DomainAddress) -> "AddressModel":
        return AddressModel(
            addressid=address.id, typeid=address.type_id, address=address.address
        )
