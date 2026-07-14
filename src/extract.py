import json
from pathlib import Path
import requests
import time
from datetime import datetime, timedelta, timezone
import sqlite3

BASE_URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
DB_PATH = Path("crypto_prices.db")

COINS = {"bitcoin": "Bitcoin",
         "ethereum": "Ethereum"
}

CURRENCY = "usd"
INITIAL_LOOKBACK_DAYS = 7

def get_latest_timestamp(coin_id):
    """
    Return the newest stored timestamp for a coin.

    The returned value is a Unix timestamp in seconds.
    Return None when the coin has no existing observations.
    """
    query = """
        SELECT MAX(o.price_timestamp) AS latest_timestamp
        FROM crypto_price_observations AS o
        JOIN coins AS c
            ON o.coin_key = c.coin_key
        WHERE c.coin_id = ?
    """

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(query, (coin_id,)).fetchone()

    if row is  None or row["latest_timestamp"] is None:
        return None
    
    stored_timestamp = row["latest_timestamp"]

        # Handle ISO-style timestamps stored as text.
    if isinstance(stored_timestamp, str):
        cleaned_timestamp = stored_timestamp.replace("Z", "+00:00")

        try:
            parsed_timestamp = datetime.fromisoformat(cleaned_timestamp)

            if parsed_timestamp.tzinfo is None:
                parsed_timestamp = parsed_timestamp.replace(
                    tzinfo=timezone.utc
                )

            return int(parsed_timestamp.timestamp())

        except ValueError as error:
            raise ValueError(
                f"Could not parse stored timestamp: {stored_timestamp}"
            ) from error

    # Handle timestamps stored numerically.
    numeric_timestamp = float(stored_timestamp)

    # CoinGecko returns timestamps in milliseconds. If your database also
    # stores milliseconds, convert them to seconds for the range request.
    if numeric_timestamp > 10_000_000_000:
        numeric_timestamp /= 1000

    return int(numeric_timestamp)

def build_time_range(coin_id):
    """
    Build the Unix timestamp rangfe for next API request
    """
    latest_timestamp = get_latest_timestamp(coin_id)
    current_timestamp = int(time.time())

    if latest_timestamp is None:
        start_datetime = datetime.now(timezone.utc) -timedelta(
            days = INITIAL_LOOKBACK_DAYS
        )
        start_timestamp = int(start_datetime.timestamp())

        print(
            f"No stored data found for {coin_id}. "
            f"Fetching the previous {INITIAL_LOOKBACK_DAYS} days."
        )
    else:
        start_timestamp = latest_timestamp + 1

        latest_display = datetime.fromtimestamp(
            latest_timestamp,
            tz=timezone.utc,
        )

        print(
            f"Latest stored {coin_id} timestamp: "
            f"{latest_display.isoformat()}"
        )

    return start_timestamp, current_timestamp

def extract_coin_data(coin_id):
    """
    Extract market chart data for one cryptocurrency
    """
    start_timestamp, end_timestamp = build_time_range(coin_id)

    url = BASE_URL.format(coin_id=coin_id)
    
    params = {
        "vs_currency": CURRENCY,
        "from": start_timestamp,
        "to": end_timestamp,
    }

    response = requests.get(url, params = params, timeout = 30)
    response.raise_for_status()

    print(
        f"Fetched {len(data.get('prices', []))} "
        f"new observations for {coin_id}."
    )
    data = response.json()
    return data

def save_raw_data(data, coin_id):
    """Save raw API response as a JSON file
    """

    output_path = Path(f"data/raw/{coin_id}_raw.json")
    output_path.parent.mkdir(parents=True, exist_ok = True)

    with open(output_path, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent = 4)

    print(f"Saved raw data for {coin_id}")

def extract_all_coins():
    """
    Extract and save raw data for all configured cryptocurrencies.
    """
    
    for coin_id in COINS:
        try:
            data = extract_coin_data(coin_id)
            save_raw_data(data, coin_id)

        except requests.RequestException as error:
            print(f"CoinGecko request failed for {coin_id}: {error}")

        except (sqlite3.Error, ValueError) as error:
            print(f"Database/timestamp error for {coin_id}: {error}")
        
    print("Incremental extraction complete")

if __name__ == "__main__":
    extract_all_coins()