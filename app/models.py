from sqlalchemy import Column, Integer, Numeric, TIMESTAMP, text, String
from .db import Base


class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    open = Column(Numeric(10, 2), nullable=False)
    high = Column(Numeric(10, 2), nullable=False)
    low = Column(Numeric(10, 2), nullable=False)
    close = Column(Numeric(10, 2), nullable=False)
    volume = Column(Integer, nullable=False)
    instrument = Column(String(50), nullable=False, index=True)
