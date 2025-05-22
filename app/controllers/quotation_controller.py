from fastapi import APIRouter, HTTPException,BackgroundTasks
from app.schemas.quotation_schema import QuotationCreate, QuotationResponse,TmpQuotationModel
from app.services.quotation_service import QuotationService
from typing import List

router = APIRouter(prefix="/quotations", tags=["Quotations"])
service = QuotationService()

@router.post("/", response_model=QuotationResponse)
async def create_quotation(data: QuotationCreate):
    return await service.create(data)

@router.get("/", response_model=List[QuotationResponse])
async def get_quotations():
    return await service.get_all()

@router.get("/{quotation_id}", response_model=QuotationResponse)
async def get_quotation(quotation_id: str):
    quotation = await service.get_by_id(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation

@router.post("/tmp_quotation/")
async def create_tmp_quotation(tmp_quotation: TmpQuotationModel):
    await service.save_tmp_quotation(tmp_quotation)
    return {"message": "Temporary quotation saved"}

@router.post("/sync_quotation/")
async def sync_quotation(background_tasks: BackgroundTasks):
    background_tasks.add_task(service.sync_tmp_to_main_quotation)
    return {"message": "Sync process started in background"}