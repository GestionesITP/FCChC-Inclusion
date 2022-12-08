from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class Rejection(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "inclusion_case_rejection"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date = Column(DateTime(timezone=True), nullable=False)
    analyst_id = Column(Integer, nullable=False)
    analyst_names = Column(String(120), nullable=False)
    comments = Column(String(800), nullable=False)
