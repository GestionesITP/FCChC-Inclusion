from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from ...helpers.schema import AreaResponse, Attachment, BussinessResponse, ConstructionResponse, EmployeeResponse, UserResponse
from ..charge_methods.schema import ChargeMethodItem
from ..approbation.schema import ApprobationItem
from ..rejection.schema import RejectionItem


class CloseBase(BaseModel):
    date: datetime
    comments: str
    assistance_id: int = Field(alias="assistanceId")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CloseCreate(CloseBase):
    pass


class CloseItem(CloseBase):
    id: int
    assistance_names: str = Field(alias="assistanceNames")
    assistance: Optional[UserResponse]


class InclusionCaseBase(BaseModel):
    date: datetime
    employee_id: int = Field(alias="employeeId")
    business_id: int = Field(alias="businessId")
    billing_business_id: int = Field(alias="billingBusinessId")
    construction_id: int = Field(alias="constructionId")
    interlocutor_id: int = Field(alias="interlocutorId")
    authorizing_user: str = Field(alias="authorizingUser")
    authorizing_charge_id: int = Field(alias="authorizingChargeId")
    delegation: str
    boss_id: int = Field(alias="bossId")
    assistance_id: int = Field(alias="assistanceId")
    charge_method_id: Optional[int] = Field(alias="chargeMethodId")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class InclusionCaseItem(InclusionCaseBase):
    number: int
    status: str
    employee_rut: str = Field(alias="employeeRut")
    employee_names: str = Field(alias="employeeNames")
    business_rut: str = Field(alias="businessRut")
    business_name: str = Field(alias="businessName")
    billing_business_name: str = Field(alias="billingBusinessName")
    construction_name: str = Field(alias="constructionName")
    boss_names: str = Field(alias="bossNames")
    assistance_names: str = Field(alias="assistanceNames")
    attachment_id: Optional[int] = Field(alias="attachmentId")
    attachment: Optional[Attachment]
    is_active: bool = Field(alias="isActive")
    charge_method: ChargeMethodItem = Field(alias="chargeMethod")
    approbation_id: Optional[int] = Field(alias="approbationId")
    rejection_id: Optional[int] = Field(alias="rejectionId")
    close_id: Optional[int] = Field(alias="closeId")
    social_case_number: Optional[int] = Field(alias="socialCaseNumber")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class InclusionCaseCreate(InclusionCaseBase):
    attachment: Optional[Attachment]

    class Config:
        schema_extra = {
            "example": {
                "date": datetime.now(),
                "employeeId": 1,
                "businessId": 2,
                "constructionId": 2,
                "interlocutorId": 3,
                "authorizingUser": "Jhon Doe",
                "authorizingChargeId": 1,
                "delegation": "ANTOFAGASTA",
                "bossId": 1,
                "assistanceId": 1,
                "chargeMethodId": 2,
                "attachment": {
                    "fileName": "sdasd",
                    "fileKey": "dadsd",
                    "fileUrl": "dadssd",
                    "fileSize": "1.2 mb",
                    "uploadDate": datetime.now()
                }
            }
        }


class InclusionCaseUpdate(BaseModel):
    social_case_number: int = Field(alias="socialCaseNumber")

    class Config:
        orm_mode = True


class InclusionCaseDetails(InclusionCaseItem):
    employee: EmployeeResponse
    business: BussinessResponse
    construction: ConstructionResponse
    boss: UserResponse
    assistance: UserResponse
    approbation: Optional[ApprobationItem]
    rejection: Optional[RejectionItem]
    close: Optional[CloseItem]
