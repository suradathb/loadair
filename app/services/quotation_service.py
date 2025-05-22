from app.database import db
from app.models.quotation_model import QuotationModel,TmpQuotationModel,AircraftModel
from app.models.customer_model import CustomerModel
from app.schemas.quotation_schema import QuotationCreate,QuotationResponse
from bson import ObjectId
from datetime import datetime, timedelta
from typing import List
from fastapi.encoders import jsonable_encoder

class QuotationService:
    def __init__(self):
        self.collection = db.quotations

    async def create(self, data: QuotationCreate) -> QuotationResponse:
        result = await self.collection.insert_one(data.dict())
        doc = await self.collection.find_one({"_id": result.inserted_id})
        return QuotationResponse(**doc)


    async def get_all(self):
        return [QuotationModel(**doc) async for doc in self.collection.find()]
                
    async def get_by_id(self, id: str):
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        return QuotationModel(**doc) if doc else None

    async def save_tmp_quotation(self,tmp_quotation: TmpQuotationModel):
        """บันทึกข้อมูล quotation ที่รับเข้ามาใน tmp collection"""
        await db.tmp_quotations.insert_one(tmp_quotation.dict(by_alias=True))


    async def sync_tmp_to_main_quotation(self,time_window_minutes: int = 10):
        """ดึงข้อมูล tmp ที่เก่ากว่าช่วงเวลาที่กำหนดมาประมวลผล"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        tmp_quotations_cursor = db.tmp_quotations.find({"received_at": {"$lte": cutoff_time}})
        tmp_quotations = await tmp_quotations_cursor.to_list(length=None)

        for tmp in tmp_quotations:
            quotation_number = tmp["quotation_number"]
            existing_quotation = await db.quotations.find_one({"quotation_number": quotation_number})

            if existing_quotation:
                await self.update_existing_quotation(existing_quotation, tmp)
            else:
                await self.create_new_quotation_and_customer(tmp)

            await db.tmp_quotations.delete_one({"_id": tmp["_id"]})


    async def update_existing_quotation(self,existing: dict, tmp: dict):
        """อัปเดต quotation และ customer หากมีการเปลี่ยนแปลง"""
        update_data = self.build_updated_quotation_fields(existing, tmp)
        
        if update_data:
            await db.quotations.update_one(
                {"_id": existing["_id"]},
                {"$set": update_data}
            )

        await self.upsert_customer(tmp)


    def build_updated_quotation_fields(self,existing: dict, tmp: dict) -> dict:
        """สร้าง dict สำหรับฟิลด์ที่เปลี่ยนแปลง"""
        fields_to_check = ["client", "currency", "conditions", "valid_until", "contact_email", "remarks"]
        update_data = {}

        for field in fields_to_check:
            if tmp.get(field) != existing.get(field):
                update_data[field] = tmp.get(field)

        if tmp.get("aircrafts") != existing.get("aircrafts"):
            update_data["aircrafts"] = tmp.get("aircrafts")

        return update_data


    async def upsert_customer(self, tmp: dict):
        """อัปเดตหรือสร้าง customer โดยใช้ company_code เป็น key"""
        company_code = tmp.get("company_code")
        if not company_code:
            raise ValueError("company_code is required to upsert customer.")

        # ค้นหาจาก company_code
        customer = await db.customers.find_one({"company_code": company_code})

        update_data = {}

        if customer:
            # ตรวจสอบ field ที่เปลี่ยนแปลง
            if tmp.get("client") and tmp.get("client") != customer.get("name"):
                update_data["name"] = tmp.get("client")

            if tmp.get("contact_email") and tmp.get("contact_email") != customer.get("email"):
                update_data["email"] = tmp.get("contact_email")

            if tmp.get("phone") and tmp.get("phone") != customer.get("phone"):
                update_data["phone"] = tmp.get("phone")

            if tmp.get("company") and tmp.get("company") != customer.get("company"):
                update_data["company"] = tmp.get("company")

            if update_data:
                await db.customers.update_one({"_id": customer["_id"]}, {"$set": update_data})
        else:
            # ถ้าไม่มี customer, ให้สร้างใหม่
            new_customer = CustomerModel(
                id=ObjectId(),
                name=tmp.get("client"),
                email=tmp.get("contact_email"),
                phone=tmp.get("phone", ""),
                company=tmp.get("company", ""),
                company_code=company_code
            )
            await db.customers.insert_one(new_customer.dict(by_alias=True))



    async def create_new_quotation_and_customer(self,tmp: dict):
        """สร้าง Quotation และ Customer ใหม่"""
        new_quotation = QuotationModel(
            id=ObjectId(),
            quotation_number=tmp.get("quotation_number"),
            client=tmp.get("client"),
            currency=tmp.get("currency"),
            aircrafts=[AircraftModel(**a) for a in tmp.get("aircrafts", [])],
            conditions=tmp.get("conditions"),
            valid_until=tmp.get("valid_until"),
            contact_email=tmp.get("contact_email"),
            remarks=tmp.get("remarks")
        )
        await db.quotations.insert_one(new_quotation.dict(by_alias=True))

        new_customer = CustomerModel(
            id=ObjectId(),
            name=tmp.get("client"),
            email=tmp.get("contact_email"),
            phone="",
            company="",
            company_code=tmp.get("company_code")
        )
        await db.customers.insert_one(new_customer.dict(by_alias=True))