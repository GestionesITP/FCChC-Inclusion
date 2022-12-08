from sqlalchemy.sql.data import func
from sqlalchemy.sql.sqltypes import DateTime
from app.database.base import Base
from sqlalchemy import Column, Integer, String


class Attachment (Base):
    __tablename__ = "attachment"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    file_name = Column(String(1024), nullable=True)
    file_key = Column(String(40), nullable=True)
    file_url = Column(String(500), nullable=True)
    file_size = Column(String(20), nullable=True)
    upload_date = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    update_at = Column(DateTime(timezone=True),
                       onupdate=func.now(), server_default=func.now())
