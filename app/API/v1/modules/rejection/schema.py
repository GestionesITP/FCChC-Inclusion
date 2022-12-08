from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from ...helpers.schema import UserResponse


class RejectionBase(BaseModel):
    date: datetime
    analyst_id: int = Field(alias="analystId")
    comments: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RejectionCreate(RejectionBase):
    pass


class RejectionItem(RejectionBase):
    id: int
    analyst_names: str = Field(alias="analystNames")


class RejectionDetails(RejectionItem):
    analyst: UserResponse
