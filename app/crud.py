from sqlalchemy.orm import Session
from . import models, schemas


def get_all_stock_data(db: Session):
    return db.query(models.StockData).order_by(models.StockData.datetime).all()


def create_stock_data(db: Session, stock_data: schemas.StockDataCreate):
    db_stock_data = models.StockData(**stock_data.model_dump())
    db.add(db_stock_data)
    db.commit()
    db.refresh(db_stock_data)
    return db_stock_data
