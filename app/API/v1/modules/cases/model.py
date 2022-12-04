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



class Closing(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "inclusion_case_close"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date = Column(DateTime(timezone=True), nullable=False)
    comments =Column(String(800), nullable=False)
    assistance_id = Column(Integer, nullable=False)
    assistance_names = Column(String(150), nullable=False)
