import pandas as pd
from typing import List
from . import schemas  # not really needed but safe-fall

### FLOW~
# First, we guard the data to make sure that there is atleast enough data to perform calculation
# Prepare the data: Convert the list of objs into pandas dataframe, only using the columns we need
#   , we also set datetime for time-series analysis
# Use a rolling window and calculate the short and long-term averages
# Generate trading signals where market share is either "buy" (1) or "sell" (-1) NO 0
# Detect the exact moment when a crossover happens~
# (.diff) calculates the change in the signal from one day to a new one

# a "buy" signal is when the state flips from -1 to 1 (a difference of 2)
# a "sell" signal is when the state flips from 1 to -1 (a difference of -2)

# Calculate performance: a complete trade requires both a buy and a sell, so we take a minimum count of the two

# Calculate a simple profit/loss by summing the difference between sell and buy prices.

# Finally; packaging the results into JSON response


def calculate_moving_average_performance(
    data: List[schemas.StockData], short_window: int = 20, long_window: int = 50
):
    if len(data) < long_window:
        return {"error": "not enough data to calculate performance"}

    df_data = [{"datetime": d.datetime, "close": d.close} for d in data]
    df = pd.DataFrame(df_data)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").sort_index()

    df["short_ma"] = df["close"].rolling(window=short_window).mean()
    df["long_ma"] = df["close"].rolling(window=long_window).mean()

    df["signal"] = -1  # defaulting to sell sig
    df.loc[df["short_ma"] > df["long_ma"], "signal"] = (
        1  # set "buy" signal where short_ma is greater
    )

    df["position"] = df["signal"].diff()

    buys = df[df["position"] == 2]
    sells = df[df["position"] == -2]

    total_trades = min(len(buys), len(sells))

    if total_trades == 0:
        return {
            "message": "no trades generated",
            "total_trades": 0,
            "total_profit_loss": 0,
        }

    profit = 0
    for i in range(total_trades):
        profit += sells.iloc[i]["close"] - buys.iloc[i]["close"]

    return {
        "strategy": "moving_average_crossover",
        "short_window": short_window,
        "long_window": long_window,
        "total_trades": total_trades,
        "total_profit_loss": float(profit),
        "signals": {
            "buys": buys.index.strftime("%Y-%m-%d").tolist(),
            "sells": sells.index.strftime("%Y-%m-%d").tolist(),
        },
    }
