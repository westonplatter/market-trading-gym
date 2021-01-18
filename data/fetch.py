import json
from os import environ

import pandas as pd
import requests

symbol = "SPY"
interval = "1min"

params = {
    "symbol": symbol,
    "apikey": environ["ALPHAADVANTAGE"],
    "function": "TIME_SERIES_INTRADAY",
    "interval": interval,
    "outputsize": "full",
}

url = "https://www.alphavantage.co/query"
res = requests.get(url, params=params)

key = f"Time Series ({interval})"
ts = res.json()[key]

result = []

for time_str, data in ts.items():
    dp = {"timestamp": time_str}
    for k, v in data.items():
        field = k.split(" ")[1]
        dp[field] = v
    result.append(dp)

df = pd.DataFrame(result)
fn = f"symbol={symbol}_interval={interval}.parquet"
df.to_parquet(fn)

msg = f"Successfully saved {symbol} data to {fn}"
print(msg)
