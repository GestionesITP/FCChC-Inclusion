from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from ...helpers.schema import Attachment, UserResponse


class ApprobationAttachment(Attachment):
    attachment_name: Optional[str] = Field(alias="attachmentName")


class ApprobationBase(BaseModel):
    date: datetime
    analyst_id: int = Field(alias="analystId")
    comments: Optional[str]
    attachments: List[ApprobationAttachment]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ApprobationCreate(ApprobationBase):
    pass


class ApprobationAttachmentItem(BaseModel):
    id: int
    date: datetime
    attachment: Attachment
    attachment_name: Optional[str] = Field(alias="attachmentName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ApprobationItem(ApprobationBase):
    id: int
    analyst_names: str = Field(alias="analystNames")
    attachments: Optional[List[ApprobationAttachmentItem]]


class ApprobationDetails(ApprobationItem):
    analyst: UserResponse
