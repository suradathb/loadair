from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from app.models.common import PyObjectId

class CustomerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: str
    phone: str
    company: str
    company_code: str  # <- เพิ่มตรงนี้

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
