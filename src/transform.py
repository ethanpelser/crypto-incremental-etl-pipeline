import json
from pathlib import Path
import pandas as pd


COINS = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum"
}

CURRENCY = "usd"

def transform_coin_data(coin_id, coin_name):
    """Load the raw data, clean it and save it as csv
    """

    raw_file = Path(f"data/raw/{coin_id}_raw.json")

    with open(raw_file, "r", encoding = "utf-8") as file:
        data = json.load(file)

    prices = pd.DataFrame(
        data["prices"],
        columns = ["timestamp_ms", "price"]
    )

    market_caps = pd.DataFrame(
        data["market_caps"],
        columns=["timestamp_ms", "market_cap"]
    )

    volumes = pd.DataFrame(
        data["total_volumes"],
        columns= ["timestamp_ms", "total_volume"]
    )

    df = prices.merge(market_caps, on = "timestamp_ms")
    df = df.merge(volumes, on = "timestamp_ms")

    df["coin_id"] = coin_id
    df["coin_name"] = coin_name
    df["currency_code"] = CURRENCY
    df["price_timestamp"] = (
        pd.to_datetime(
            df["timestamp_ms"],
            unit="ms",
            utc=True,
        )
        .dt.floor("s")
    )

    df = df[[
        "coin_id",
        "coin_name",
        "currency_code",
        "price_timestamp",
        "price",
        "market_cap",
        "total_volume"
    ]]

    df =df.drop_duplicates(
        subset = ["coin_id", "currency_code", "price_timestamp"]
    )

    df = df.dropna(
        subset = ["coin_id", "currency_code", "price_timestamp"]
    )
    
    return df

def transform_all_coins():
    """
    Transform all raw coin JSON files into one cleaned CSV.
    """

    frames = []

    for coin_id, coin_name in COINS.items():
        coins_df = transform_coin_data(coin_id, coin_name)
        frames.append(coins_df)

    final_df = pd.concat(frames, ignore_index= True)

    output_path = Path("data/processed/crypto_prices_cleaned.csv")
    output_path.parent.mkdir(parents= True, exist_ok = True)

    final_df.to_csv(output_path, index = False)

    print(f"Transformed {len(final_df)} rows.")

    return final_df

if __name__ == "__main__":
    transform_all_coins()