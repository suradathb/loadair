from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company: str
    company_code: str  # <- เพิ่มตรงนี้

class CustomerResponse(CustomerCreate):
    id: str
