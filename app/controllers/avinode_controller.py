from fastapi import APIRouter, HTTPException
from app.models.avinode_rfq import AvinodeRFQ
from app.services.avinode_service import convert_rfq_to_quotation_and_customer

router = APIRouter(prefix="/integration", tags=["Avinode Integration"])

@router.post("/avinode/rfq")
async def receive_rfq_from_avinode(rfq: AvinodeRFQ):
    try:
        customer, quotation = convert_rfq_to_quotation_and_customer(rfq)
        
        # TODO: save to DB
        print("Customer:", customer)
        print("Quotation:", quotation)

        return {
            "message": "RFQ processed successfully",
            "customer": customer,
            "quotation": quotation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
