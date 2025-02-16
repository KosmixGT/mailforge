# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
metadata = Base.metadata


class Deliverystatus(Base):
    __tablename__ = "deliverystatuses"

    deliverystatusid = Column(
        Integer,
        primary_key=True,
        server_default=text(
            "nextval('deliverystatuses_deliverystatusid_seq'::regclass)"
        ),
    )
    statusname = Column(String(50), nullable=False, unique=True)


class Mailingstatus(Base):
    __tablename__ = "mailingstatuses"

    statusid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('mailingstatuses_statusid_seq'::regclass)"),
    )
    statusname = Column(String(50), nullable=False, unique=True)


class Mailingtype(Base):
    __tablename__ = "mailingtypes"

    typeid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('mailingtypes_typeid_seq'::regclass)"),
    )
    typename = Column(String(50), nullable=False, unique=True)


class Template(Base):
    __tablename__ = "templates"

    templateid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('templates_templateid_seq'::regclass)"),
    )
    name = Column(String(100), nullable=False)
    messagetext = Column(Text, nullable=False)


class Userrole(Base):
    __tablename__ = "userroles"

    roleid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('userroles_roleid_seq'::regclass)"),
    )
    rolename = Column(String(50), nullable=False, unique=True)


class Address(Base):
    __tablename__ = "addresses"

    addressid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('addresses_addressid_seq'::regclass)"),
    )
    typeid = Column(
        ForeignKey("mailingtypes.typeid", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    address = Column(String(255), nullable=False, unique=True)

    mailingtype = relationship("Mailingtype")


class User(Base):
    __tablename__ = "users"

    userid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('users_userid_seq'::regclass)"),
    )
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    roleid = Column(ForeignKey("userroles.roleid"), nullable=False)

    userrole = relationship("Userrole")


class Mailing(Base):
    __tablename__ = "mailings"

    mailingid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('mailings_mailingid_seq'::regclass)"),
    )
    userid = Column(ForeignKey("users.userid"), nullable=False)
    title = Column(String(255), nullable=False)
    messagetext = Column(Text, nullable=False)
    scheduledtime = Column(DateTime)
    statusid = Column(ForeignKey("mailingstatuses.statusid"), nullable=False)

    mailingstatus = relationship("Mailingstatus")
    user = relationship("User")


class Mailinghistory(Base):
    __tablename__ = "mailinghistory"

    historyid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('mailinghistory_historyid_seq'::regclass)"),
    )
    mailingid = Column(ForeignKey("mailings.mailingid"), nullable=False)
    senttime = Column(DateTime, nullable=False)
    deliverystatusid = Column(ForeignKey("deliverystatuses.deliverystatusid"))

    deliverystatus = relationship("Deliverystatus")
    mailing = relationship("Mailing")


class Recipient(Base):
    __tablename__ = "recipients"

    recipientid = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('recipients_recipientid_seq'::regclass)"),
    )
    mailingid = Column(
        ForeignKey("mailings.mailingid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    addressid = Column(
        ForeignKey("addresses.addressid", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    deliverystatusid = Column(
        ForeignKey(
            "deliverystatuses.deliverystatusid", ondelete="SET NULL", onupdate="CASCADE"
        )
    )
    historyid = Column(
        ForeignKey("mailinghistory.historyid", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    address = relationship("Address")
    deliverystatus = relationship("Deliverystatus")
    mailinghistory = relationship("Mailinghistory")
    mailing = relationship("Mailing")
