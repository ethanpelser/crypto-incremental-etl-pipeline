import json
from pathlib import Path
import requests

BASE_URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

COINS = {"bitcoin": "Bitcoin",
         "ethereum": "Ethereum"
}

CURRENCY = "usd"
DAYS = "7"

def extract_coin_data(coin_id):
    """
    Extract market chart data for one cryptocurrency
    """

    url= BASE_URL.format(coin_id = coin_id)
    params = {
        "vs_currency": CURRENCY,
        "days": DAYS
    }

    response = requests.get(url, params = params, timeout = 30)
    response.raise_for_status()

    return response.json()

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
        data = extract_coin_data(coin_id)
        save_raw_data(data, coin_id)

    print("extraction complete")

if __name__ == "__main__":
    extract_all_coins()