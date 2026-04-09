from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.services.local_storage_service import create_payment_order, verify_payment_and_activate

router = APIRouter(tags=['payment'])


class CreateOrderRequest(BaseModel):
    email: EmailStr
    amount: int | None = None


class VerifyPaymentRequest(BaseModel):
    email: EmailStr
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


@router.post('/api/payment/create-order')
def payment_create_order(payload: CreateOrderRequest):
    try:
        return create_payment_order(payload.email, payload.amount)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post('/api/payment/verify')
def payment_verify(payload: VerifyPaymentRequest):
    try:
        return verify_payment_and_activate(
            email=payload.email,
            razorpay_order_id=payload.razorpay_order_id,
            razorpay_payment_id=payload.razorpay_payment_id,
            razorpay_signature=payload.razorpay_signature,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
