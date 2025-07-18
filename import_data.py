import pandas as pd
from app.db import SessionLocal, engine
from app.models import StockData, Base


def import_data_from_csv(filepath: str):
    db = SessionLocal()
    try:
        print("reading csv data...")
        df = pd.read_csv(filepath)
        df = df[["datetime", "open", "high", "low", "close", "volume", "instrument"]]
        df["datetime"] = pd.to_datetime(df["datetime"])

        data_to_insert = df.to_dict(orient="records")

        print(f"inserting {len(data_to_insert)} records into the database...")
        db.bulk_insert_mappings(StockData, data_to_insert)
        db.commit()
        print("data import successful!")

    except Exception as e:
        db.rollback()
        print(f"an error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("creating database tables...")
    Base.metadata.create_all(bind=engine)
    import_data_from_csv("data/stock_data.csv")
