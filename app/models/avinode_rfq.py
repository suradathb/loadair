from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class AvinodeAircraft(BaseModel):
    tail_number: str
    aircraft_type: str
    lease_term: str
    monthly_rate: float

class AvinodeRFQ(BaseModel):
    rfq_id: str
    client_name: str
    client_email: EmailStr
    client_phone: Optional[str]
    company_name: Optional[str]
    aircrafts: List[AvinodeAircraft]
    currency: str
    conditions: Optional[str]
    valid_until: datetime
    remarks: Optional[str]
