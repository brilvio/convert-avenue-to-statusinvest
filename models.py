from enum import Enum

from pydantic import BaseModel

from consts import SYMBOLS


class TypeAvenueOperation(Enum):
    BOUGHT = "BOUGHT"
    SOLD = "SOLD"


class AvenueOperation(BaseModel):
    type_operation: TypeAvenueOperation
    date: str
    description: str
    symbol: str
    quantity: float
    price: float

    @classmethod
    def build_operation(
        cls,
        type_operation: TypeAvenueOperation,
        date: str,
        description: str,
        quantity: float,
        price: float,
    ):
        symbol = SYMBOLS.get(description, "unknown")

        return cls(
            type_operation=type_operation,
            date=date,
            description=description,
            symbol=symbol,
            quantity=quantity,
            price=price,
        )
