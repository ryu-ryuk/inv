import unittest
from datetime import datetime, timedelta
from app.strategy import calculate_moving_average_performance
from app.schemas import StockData


class TestStrategyCalculation(unittest.TestCase):
    def test_moving_average_logic(self):
        """test the moving average crossover logic with predictable data."""
        mock_data = []
        base_date = datetime(2025, 1, 1)

        # stable price
        for i in range(30):
            current_date = base_date + timedelta(days=i)
            mock_data.append(
                StockData(
                    id=i,
                    datetime=current_date,
                    open=100,
                    high=100,
                    low=100,
                    close=100,
                    volume=1000,
                    instrument="MOCK",
                )
            )

        # dip
        for i in range(30, 60):
            current_date = base_date + timedelta(days=i)
            mock_data.append(
                StockData(
                    id=i,
                    datetime=current_date,
                    open=90,
                    high=90,
                    low=90,
                    close=90,
                    volume=1000,
                    instrument="MOCK",
                )
            )

        # spike
        for i in range(60, 90):
            current_date = base_date + timedelta(days=i)
            mock_data.append(
                StockData(
                    id=i,
                    datetime=current_date,
                    open=110,
                    high=110,
                    low=110,
                    close=110,
                    volume=1000,
                    instrument="MOCK",
                )
            )

        # final dip
        for i in range(90, 120):
            current_date = base_date + timedelta(days=i)
            mock_data.append(
                StockData(
                    id=i,
                    datetime=current_date,
                    open=80,
                    high=80,
                    low=80,
                    close=80,
                    volume=1000,
                    instrument="MOCK",
                )
            )

        result = calculate_moving_average_performance(
            mock_data, short_window=10, long_window=30
        )

        # the test assertions is the same
        self.assertIn("total_trades", result)
        self.assertGreater(result["total_trades"], 0)
