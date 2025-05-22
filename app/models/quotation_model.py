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

class QuotationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    quotation_number: str
    client: str
    currency: str
    aircrafts: List[AircraftModel]
    conditions: str
    valid_until: datetime
    contact_email: Optional[EmailStr] = None
    remarks: Optional[str] = None

    class Config:
        allow_population_by_field_name = True   # แก้ตรงนี้
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TmpQuotationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    quotation_number: str
    client: str
    currency: str
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