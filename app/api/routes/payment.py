import os
import httpx
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from app.schemas.payment_schema import KhaltiInitiateRequest
from pydantic import BaseModel
from datetime import datetime
import uuid

load_dotenv()

router = APIRouter()

KHALTI_SECRET_KEY = os.getenv("KHALTI_SECRET_KEY")
KHALTI_INITIATE_URL = "https://a.khalti.com/api/v2/epayment/initiate/"


@router.post("/khalti/initiate")
async def initiate_khalti_payment(request: KhaltiInitiateRequest):
    if not KHALTI_SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="Khalti secret key is not configured"
        )

    payload = {
        "return_url": "https://example.com/payment-success",
        "website_url": "https://example.com",
        "amount": request.amount,
        "purchase_order_id": request.purchase_order_id,
        "purchase_order_name": request.purchase_order_name,
        "customer_info": {
            "name": request.customer_name,
            "email": request.customer_email,
            "phone": request.customer_phone,
        },
    }

    headers = {
        "Authorization": f"Key {KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            KHALTI_INITIATE_URL,
            json=payload,
            headers=headers,
            timeout=20,
        )

    if response.status_code not in [200, 201]:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    return response.json()


class KhaltiLookupRequest(BaseModel):
    pidx: str


KHALTI_LOOKUP_URL = "https://a.khalti.com/api/v2/epayment/lookup/"


@router.post("/khalti/lookup")
async def lookup_khalti_payment(request: KhaltiLookupRequest):
    if not KHALTI_SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="Khalti secret key is not configured"
        )

    headers = {
        "Authorization": f"Key {KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "pidx": request.pidx
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            KHALTI_LOOKUP_URL,
            json=payload,
            headers=headers,
            timeout=20,
        )

    if response.status_code not in [200, 201]:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    result = response.json()

    return {
        "success": result.get("status") == "Completed",
        "status": result.get("status"),
        "data": result
    }




# esewa mock payment endpoint for testing without real transactions
class EsewaMockPaymentRequest(BaseModel):
    amount: int
    purchase_order_id: str
    purchase_order_name: str
    customer_phone: str


@router.post("/esewa/mock-pay")
def esewa_mock_payment(request: EsewaMockPaymentRequest):
    transaction_id = f"ESEWA-{uuid.uuid4().hex[:10].upper()}"

    return {
        "message": "eSewa mock payment successful",
        "success": True,
        "payment_method": "esewa",
        "transaction_id": transaction_id,
        "amount": request.amount,
        "purchase_order_id": request.purchase_order_id,
        "purchase_order_name": request.purchase_order_name,
        "customer_phone": request.customer_phone,
        "paid_at": datetime.now().isoformat(),
    }