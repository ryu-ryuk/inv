from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, strategy
from .db import SessionLocal, engine

# create db tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Invsto Backend Assignment")


# dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/data", response_model=schemas.StockData, status_code=201)
def create_data_entry(
    stock_data: schemas.StockDataCreate, db: Session = Depends(get_db)
):
    """adds a new stock data record to the database."""
    return crud.create_stock_data(db=db, stock_data=stock_data)


@app.get("/data", response_model=List[schemas.StockData])
def read_all_data(db: Session = Depends(get_db)):
    """fetches all stock data records from the database."""
    return crud.get_all_stock_data(db=db)


@app.get("/strategy/performance")
def get_strategy_performance(db: Session = Depends(get_db)):
    """calculates and returns the performance of the moving average crossover strategy."""
    all_data = crud.get_all_stock_data(db)
    if not all_data:
        raise HTTPException(status_code=404, detail="no stock data found in database")

    performance_report = strategy.calculate_moving_average_performance(all_data)
    return performance_report
