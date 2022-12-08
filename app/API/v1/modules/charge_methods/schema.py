from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ChargeMethodBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = False


class ChargeMethodCreate(ChargeMethodBase):
    pass


class ChargeMethodItem(ChargeMethodBase):
    id: int
    created_at: datetime = Field(alias="createdDate")
    is_active: bool = Field(alias="")


class User(BaseModel):
    user_id: int = Field(alias="userName")
    user_names: str = Field(alias="userId")

    class Config:
        orm_mode = True
        allow_population_by_field_name = False


class AnswerBase(BaseModel):
    area_id: int = Field(alias="areaId")
    area_name: str = Field(alias="areaName")
    channel: str
    answer: str
    topic_id: int = Field(alias="topicId")
    topic_name: str = Field(alias="topicName")
    date: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
