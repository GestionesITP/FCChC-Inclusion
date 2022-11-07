from sqlalchemy.sql.sqltypes import Boolean
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class ChargeMethod(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "charge_method"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(120), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
