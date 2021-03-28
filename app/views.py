from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.models import Transaction, Wallet, database
from app.schemas import (
    AddMoneyRequest,
    BaseResponse,
    CreateWalletRequest,
    SendMoneyRequest,
)

router = APIRouter()


@router.post("/wallet")
@database.transaction()
async def create_wallet(request: CreateWalletRequest):
    wallet = Wallet(client_id=request.client_id, amount=0, currency=request.currency)

    await wallet.create()

    return BaseResponse(success=True, errors=[], result={"wallet": wallet})


@router.post("/money/add")
@database.transaction()
async def add_money(request: AddMoneyRequest):
    wallet = await Wallet.get_for_update(request.wallet_id)

    if wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet(id={request.wallet_id}) not found",
        )

    tr = Transaction(
        from_wallet_id=None,
        to_wallet_id=wallet.id,
        request_id=request.request_id,
        amount=request.amount,
        currency=request.currency,
    )
    await tr.create()
    await wallet.update_amount(request.amount)
    return BaseResponse(success=True, errors=[], result={"wallet": wallet, "tr": tr})


@router.post("/money/send")
@database.transaction()
async def send_money(request: SendMoneyRequest):
    if request.from_wallet_id < request.to_wallet_id:
        wallet_from = await Wallet.get_for_update(request.from_wallet_id)
        wallet_to = await Wallet.get_for_update(request.to_wallet_id)
    else:
        wallet_to = await Wallet.get_for_update(request.to_wallet_id)
        wallet_from = await Wallet.get_for_update(request.from_wallet_id)

    if wallet_from is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet(id={request.from_wallet_id}) not found",
        )

    if wallet_to is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet(id={request.to_wallet_id}) not found",
        )

    if wallet_from.amount < request.amount:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="not enough money",
        )

    tr = Transaction(
        from_wallet_id=wallet_from.id,
        to_wallet_id=wallet_to.id,
        request_id=request.request_id,
        amount=request.amount,
        currency=request.currency,
    )

    await tr.create()
    await wallet_from.update_amount(-request.amount)
    await wallet_to.update_amount(request.amount)

    return BaseResponse(
        success=True,
        errors=[],
        result={"wallet_from": wallet_from, "wallet_to": wallet_to, "tr": tr},
    )
