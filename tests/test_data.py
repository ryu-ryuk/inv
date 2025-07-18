import unittest
from fastapi.testclient import TestClient
from app.main import app, get_db
from app.db import Base, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

# a separate test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# override the get_db dependency to use the test db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


class TestDataEndpoints(unittest.TestCase):
    def setUp(self):
        """create a fresh database for every single test."""
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)

    def tearDown(self):
        """drop all tables after every test."""
        Base.metadata.drop_all(bind=engine)

    def test_create_data_valid(self):
        """test creating a valid data entry."""
        response = self.client.post(
            "/data",
            json={
                "datetime": "2025-07-18T10:00:00Z",
                "open": 150.0,
                "high": 152.5,
                "low": 149.5,
                "close": 151.0,
                "volume": 100000,
                "instrument": "TEST",
            },
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()

        # compare decimal to decimal for precision
        self.assertEqual(Decimal(data["close"]), Decimal("151.0"))
        self.assertEqual(data["instrument"], "TEST")

    def test_read_all_data(self):
        """test fetching data after creating it."""
        # first, adding some data
        self.client.post(
            "/data",
            json={
                "datetime": "2025-07-18T12:00:00Z",
                "open": 160.0,
                "high": 162.5,
                "low": 159.5,
                "close": 161.0,
                "volume": 200000,
                "instrument": "TEST",
            },
        )

        # now, get the data
        response = self.client.get("/data")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # assert that we got the one record we created
        self.assertEqual(len(data), 1)
        self.assertEqual(Decimal(data[0]["close"]), Decimal("161.0"))
