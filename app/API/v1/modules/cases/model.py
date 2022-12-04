from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String
from ...helpers.model import Attachment


class InclusionCase(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "inclusion_case"
    number = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date = Column(DateTime(timezone=True), nullable=False)
    employee_rut = Column(String(12), nullable=False)
    employee_id = Column(Integer, nullable=False)
    employee_names = Column(String(250), nullable=False)
    business_rut = Column(String(12), nullable=False)
    business_id = Column(Integer, nullable=False)
    business_name = Column(String(120), nullable=False)
    construction_id = Column(Integer, nullable=False)
    construction_name = Column(String(120), nullable=False)
    billing_business_id = Column(Integer, nullable=False)
    billing_business_name = Column(String(120), nullable=False)
    interlocutor_id = Column(Integer, nullable=False)
    authorizing_user = Column(String(250), nullable=False)
    authorizing_charge_id = Column(Integer, nullable=False)
    status = Column(String(25), nullable=False)
    delegation = Column(String(120), nullable=False)
    boss_id = Column(Integer, nullable=False)
    boss_names = Column(String(120), nullable=False)
    assistance_id = Column(Integer, nullable=False, server_default="1")
    assistance_names = Column(
        String(120), nullable=False, server_default="ADMIN MYERS")
    is_active = Column(Boolean, nullable=False, server_default="1")
    charge_method_id = Column(Integer, ForeignKey(
        "charge_method.id"), nullable=False)
    attachment_id = Column(Integer, ForeignKey(
        "attachment.id"))
    approbation_id = Column(Integer, ForeignKey("approbation.id"))
    rejection_id = Column(Integer, ForeignKey("inclusion_case_rejection.id"))
    close_id = Column(Integer, ForeignKey("inclusion_case_close.id"))
    social_case_number = Column(Integer)
    attachment = relationship("Attachment", uselist=False, lazy="joined")
    charge_method = relationship("ChargeMethod", uselist=False, lazy="joined")
    approbation = relationship("Approbation", uselist=False, lazy="joined")
    rejection = relationship("Rejection", uselist=False, lazy="joined")
    close = relationship("Closing", uselist=False, lazy="joined")


class Closing(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "inclusion_case_close"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date = Column(DateTime(timezone=True), nullable=False)
    comments =Column(String(800), nullable=False)
    assistance_id = Column(Integer, nullable=False)
    assistance_names = Column(String(150), nullable=False)
