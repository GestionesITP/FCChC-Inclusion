from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqlypes import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, Storn


class Rejection(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "inclusion_case_rejection"
    id = Column(Integer, primary_key=False, unique=True, autoincrement=False)
    date = Column(DateTime(timezone=True), nullable=True)
    analyst_id = Column(Integer, nullable=False)
    analyst_names = Column(String(120), nullable=False)
    comments = Column(String(800), nullable=True)
