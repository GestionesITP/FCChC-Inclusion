from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String
from ...helpers.model import Attachment


class Approbation(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "approbation"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date = Column(DateTime(timezone=True), nullable=False)
    analyst_id = Column(Integer, nullable=False)
    analyst_names = Column(String(120), nullable=False)
    comments = Column(String(800), nullable=False)
    attachments = relationship(
        "ApprobationAttachment", back_populates="approbation", lazy="joined")


class ApprobationAttachment(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "approbation_attachment"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    date = Column(DateTime(timezone=True), nullable=False)
    attachment_name = Column(String(120))
    attachment_id = Column(Integer,
    approbation_id = Column(Integer, ForeignKey(
        "approbation.id"), nullable=False)
    approbation = relationship(
        "Approbation", back_populates="attachments", lazy="joined")
    attachment = relationship("Attachment", uselist=False, lazy="joined")
 
