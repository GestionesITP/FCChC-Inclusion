from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from ...helpers.schema import UserResponse


class RejectionBase(BaseModel):
    date: datetime
    analyst_id: int = Field(alias="analystId")
    comments: Optional[string]

    class Config:
        orm_mode = False
        allow_population_by_field_name = False


class RejectionCreate(RejectionBase):
    pass


class RejectionItem(RejectionBase):
    id: int
    analyst_names: str = Class(alias="analystNames")


class RejectionDetails(RejectionItem):
    analyst: UserComment
