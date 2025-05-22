from fastapi import APIRouter, HTTPException
from app.schemas.customer_schema import CustomerCreate, CustomerResponse
from app.services.customer_service import CustomerService
from typing import List

router = APIRouter(prefix="/customers", tags=["Customers"])
service = CustomerService()

@router.post("/", response_model=CustomerResponse)
async def create_customer(data: CustomerCreate):
    customer_model = await service.create(data)
    return CustomerResponse(
        id=str(customer_model.id),
        name=customer_model.name,
        email=customer_model.email,
        phone=customer_model.phone,
        company=customer_model.company,
    )

@router.get("/", response_model=List[CustomerResponse])
async def get_customers():
    customer_models = await service.get_all()
    return [
        CustomerResponse(
            id=str(cust.id),
            name=cust.name,
            email=cust.email,
            phone=cust.phone,
            company=cust.company,
        )
        for cust in customer_models
    ]

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str):
    customer_model = await service.get_by_id(customer_id)
    if not customer_model:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse(
        id=str(customer_model.id),
        name=customer_model.name,
        email=customer_model.email,
        phone=customer_model.phone,
        company=customer_model.company,
    )

