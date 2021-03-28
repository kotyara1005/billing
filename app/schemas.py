from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, root_validator, validator

from app.models import Currency


class BaseResponse(BaseModel):
    success: bool
    errors: Optional[list]
    result: Optional[dict]


class CreateWalletRequest(BaseModel):
    client_id: int
    currency: Currency


def greater_then_zero(value: Decimal):
    if value <= 0:
        raise ValueError("value should be greater then zero")
    return value


class AddMoneyRequest(BaseModel):
    wallet_id: int
    request_id: UUID
    amount: Decimal
    currency: Currency

    _amount_validator = validator("amount", allow_reuse=True)(greater_then_zero)


class SendMoneyRequest(BaseModel):
    from_wallet_id: int
    to_wallet_id: int
    request_id: UUID
    amount: Decimal
    currency: Currency

    _amount_validator = validator("amount", allow_reuse=True)(greater_then_zero)

    @root_validator
    def check_selfsender(cls, values):
        if values.get("from_wallet_id") == values.get("to_wallet_id"):
            raise ValueError("self sending")
        return values
