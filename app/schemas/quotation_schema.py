from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.models.common import PyObjectId

class AircraftModel(BaseModel):
    tail_number: str
    aircraft_type: str
    lease_term: str
    monthly_rate: float

class QuotationCreate(BaseModel):
    quotation_number: str
    client: str
    currency: str
    aircrafts: List[AircraftModel]
    conditions: str
    valid_until: datetime
    contact_email: Optional[EmailStr] = None
    remarks: Optional[str] = None

class QuotationResponse(QuotationCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

class TmpQuotationModel(BaseModel):
    quotation_number: str
    client: str
    currency: str
    company_code:str
    aircrafts: List[AircraftModel]
    conditions: str
    valid_until: datetime
    contact_email: Optional[EmailStr] = None
    remarks: Optional[str] = None
    received_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}