from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class StockDataBase(BaseModel):
    datetime: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    instrument: str


class StockDataCreate(StockDataBase):
    pass


class StockData(StockDataBase):
    id: int

    class Config:
        from_attributes = True
