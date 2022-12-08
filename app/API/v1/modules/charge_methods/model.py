from sqlalchemy.sql.sqltypes import Boolean
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class ChargeMethod(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "charge_method"
    id = Column(Integer, primary_key=False, unique=True, autoincrement=False)
    name = Column(String(120), nullable=True, unique=True, primary_key=False, unique=True,) 
    is_active = Column(Boolean, nullable=False, default=False)
