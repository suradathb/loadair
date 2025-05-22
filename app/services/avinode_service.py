from app.models.avinode_rfq import AvinodeRFQ
from app.models.quotation_model import QuotationModel, AircraftModel
from app.models.customer_model import CustomerModel
from bson import ObjectId

def convert_rfq_to_quotation_and_customer(rfq: AvinodeRFQ):
    # สร้าง Customer
    customer = CustomerModel(
        id=ObjectId(),
        name=rfq.client_name,
        email=rfq.client_email,
        phone=rfq.client_phone or "",
        company=rfq.company_name or ""
    )

    # สร้าง AircraftModel list
    aircrafts = [AircraftModel(**a.dict()) for a in rfq.aircrafts]

    # สร้าง QuotationModel
    quotation = QuotationModel(
        id=ObjectId(),
        quotation_number=f"QTN-{rfq.rfq_id}",
        client=rfq.client_name,
        currency=rfq.currency,
        aircrafts=aircrafts,
        conditions=rfq.conditions or "",
        valid_until=rfq.valid_until,
        contact_email=rfq.client_email,
        remarks=rfq.remarks
    )

    return customer, quotation
