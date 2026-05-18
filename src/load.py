import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_PATH = "crypto_prices.db"
CSV_FILE = "data/processed/crypto_prices_cleaned.csv"


def load_dimension_tables(df,engine):
    """
    Load unique coins and currencies into dimension tables
    """

    coins = df[["coin_id", "coin_name"]].drop_duplicates()
    currencies = df[["currency_code"]].drop_duplicates()

    with engine.begin() as conn:
        for _, row in coins.iterrows():
            conn.execute(
                text("""
                    INSERT OR IGNORE INTO coins (coin_id, coin_name)
                    VALUES (:coin_id, :coin_name)
                """),
                {
                    "coin_id": row["coin_id"],
                    "coin_name": row["coin_name"]
                }
            )

        for _, row in currencies.iterrows():
            conn.execute(
                text("""
                    INSERT OR IGNORE INTO currencies (currency_code)
                    VALUES (:currency_code)
                """),
                {
                    "currency_code": row["currency_code"]
                }
            )


def load_price_observations(df, engine):
    """
    Load only new price observations into the crypto_price_observations table.
    """

    coins_db = pd.read_sql(
        "SELECT coin_key, coin_id FROM coins",
        engine
    )

    currencies_db = pd.read_sql(
        "SELECT currency_key, currency_code FROM currencies",
        engine
    )

    df = df.merge(coins_db, on="coin_id", how="left")
    df = df.merge(currencies_db, on="currency_code", how="left")

    observations = df[[
        "coin_key",
        "currency_key",
        "price_timestamp",
        "price",
        "market_cap",
        "total_volume"
    ]]

    with engine.begin() as conn:
        inserted_count = 0

        for _, row in observations.iterrows():
            result = conn.execute(
                text("""
                    INSERT OR IGNORE INTO crypto_price_observations (
                        coin_key,
                        currency_key,
                        price_timestamp,
                        price,
                        market_cap,
                        total_volume
                    )
                    VALUES (
                        :coin_key,
                        :currency_key,
                        :price_timestamp,
                        :price,
                        :market_cap,
                        :total_volume
                    )
                """),
                {
                    "coin_key": int(row["coin_key"]),
                    "currency_key": int(row["currency_key"]),
                    "price_timestamp": row["price_timestamp"],
                    "price": float(row["price"]),
                    "market_cap": float(row["market_cap"]) if pd.notna(row["market_cap"]) else None,
                    "total_volume": float(row["total_volume"]) if pd.notna(row["total_volume"]) else None
                }
            )

            inserted_count += result.rowcount

    print(f"Loaded {inserted_count} new price observations.")


def load_incremental_data():
    """
    Load cleaned crypto records into normalized SQLite tables incrementally.
    """

    engine = create_engine(f"sqlite:///{DATABASE_PATH}")

    df = pd.read_csv(CSV_FILE)

    df["price_timestamp"] = pd.to_datetime(df["price_timestamp"]).astype(str)

    load_dimension_tables(df, engine)
    load_price_observations(df, engine)


if __name__ == "__main__":
    load_incremental_data()