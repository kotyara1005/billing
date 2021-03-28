from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

import databases
from pydantic import BaseModel
from app.settings import DATABASE_URL


database = databases.Database(DATABASE_URL)


class Currency(str, Enum):
    USD = "USD"


class Wallet(BaseModel):
    id: Optional[int]
    client_id: int
    amount: Decimal
    currency: Currency

    async def create(self):
        self.id = await database.fetch_val(
            """
                INSERT INTO wallet(client_id, amount, currency) 
                VALUES (:client_id, :amount, :currency)
                RETURNING id
            """,
            self.dict(exclude={'id'}),
        )

    @classmethod
    async def get_for_update(cls, wallet_id: int) -> Optional['Wallet']:
        row = await database.fetch_one(
            """
                SELECT id, client_id, amount, currency
                FROM wallet
                WHERE id=:wallet_id
                FOR UPDATE
            """,
            dict(wallet_id=wallet_id)
        )
        if row is None:
            return None
        return Wallet(**row)

    async def update_amount(self, diff):
        await database.execute(
            """
                UPDATE wallet
                SET amount = amount + :diff
                WHERE id=:wallet_id
            """,
            dict(wallet_id=self.id, diff=diff)
        )
        self.amount += diff


class Transaction(BaseModel):
    """"""
    id: Optional[int]
    from_wallet_id: Optional[int]
    to_wallet_id: int
    request_id: UUID
    amount: Decimal
    currency: Currency

    async def create(self):
        self.id = await database.fetch_val(
            """
                INSERT INTO transaction(from_wallet_id, to_wallet_id, request_id, amount, currency) 
                VALUES (:from_wallet_id, :to_wallet_id, :request_id, :amount, :currency)
                RETURNING id
            """,
            self.dict(exclude={'id'}),
        )
