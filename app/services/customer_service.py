from app.database import db
from app.models.customer_model import CustomerModel
from app.schemas.customer_schema import CustomerCreate,CustomerResponse
from bson import ObjectId

class CustomerService:
    def __init__(self):
        self.collection = db.customers

    async def create(self, data: CustomerCreate) -> CustomerResponse:
        result = await self.collection.insert_one(data.dict())
        doc = await self.collection.find_one({"_id": result.inserted_id})
        doc["_id"] = str(doc["_id"])
        return CustomerResponse(
            id=doc["_id"],
            name=doc["name"],
            email=doc["email"],
            phone=doc["phone"],
            company=doc["company"],
        )

    async def get_all(self) -> list[CustomerResponse]:
        customers = []
        async for doc in self.collection.find():
            doc["_id"] = str(doc["_id"])
            customers.append(CustomerResponse(
                id=doc["_id"],
                name=doc["name"],
                email=doc["email"],
                phone=doc["phone"],
                company=doc["company"],
            ))
        return customers

    async def get_by_id(self, id: str) -> CustomerResponse | None:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return CustomerResponse(
            id=doc["_id"],
            name=doc["name"],
            email=doc["email"],
            phone=doc["phone"],
            company=doc["company"],
        )
