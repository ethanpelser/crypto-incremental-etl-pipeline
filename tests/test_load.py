import pandas as pd
from sqlalchemy import create_engine, text

import load


CREATE_TABLES_SQL = """
CREATE TABLE coins(
    coin_key INTEGER PRIMARY KEY AUTOINCREMENT,
    coin_id TEXT NOT NULL UNIQUE,
    coin_name TEXT NOT NULL UNIQUE
);

CREATE TABLE currencies(
    currency_key INTEGER PRIMARY KEY AUTOINCREMENT,
    currency_code TEXT NOT NULL UNIQUE
);

CREATE TABLE crypto_price_observations(
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin_key INTEGER NOT NULL,
    currency_key INTEGER NOT NULL,
    price_timestamp TEXT NOT NULL,
    price REAL NOT NULL,
    market_cap REAL,
    total_volume REAL,
    loaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (coin_key) REFERENCES coins(coin_key),
    FOREIGN KEY (currency_key) REFERENCES currencies(currency_key),
    UNIQUE (price_timestamp, currency_key, coin_key)
);
"""


def make_engine():
    engine = create_engine("sqlite:///:memory:")
    raw_conn = engine.raw_connection()
    try:
        raw_conn.executescript(CREATE_TABLES_SQL)
        raw_conn.commit()
    finally:
        raw_conn.close()
    return engine


def sample_clean_df():
    return pd.DataFrame(
        [
            {
                "coin_id": "bitcoin",
                "coin_name": "Bitcoin",
                "currency_code": "usd",
                "price_timestamp": "2023-11-14 22:13:20",
                "price": 50000.0,
                "market_cap": 900000000.0,
                "total_volume": 30000000.0,
            },
            {
                "coin_id": "ethereum",
                "coin_name": "Ethereum",
                "currency_code": "usd",
                "price_timestamp": "2023-11-14 22:13:20",
                "price": 2500.0,
                "market_cap": 300000000.0,
                "total_volume": 10000000.0,
            },
        ]
    )


def scalar(engine, sql):
    with engine.connect() as conn:
        return conn.execute(text(sql)).scalar_one()


def test_load_dimension_tables_inserts_unique_coins_and_currencies():
    engine = make_engine()
    df = pd.concat([sample_clean_df(), sample_clean_df()], ignore_index=True)

    load.load_dimension_tables(df, engine)

    assert scalar(engine, "SELECT COUNT(*) FROM coins") == 2
    assert scalar(engine, "SELECT COUNT(*) FROM currencies") == 1


def test_load_price_observations_inserts_rows_with_dimension_keys():
    engine = make_engine()
    df = sample_clean_df()
    load.load_dimension_tables(df, engine)

    load.load_price_observations(df, engine)

    assert scalar(engine, "SELECT COUNT(*) FROM crypto_price_observations") == 2
    assert scalar(engine, "SELECT COUNT(*) FROM crypto_price_observations WHERE coin_key IS NULL") == 0
    assert scalar(engine, "SELECT COUNT(*) FROM crypto_price_observations WHERE currency_key IS NULL") == 0


def test_load_price_observations_is_incremental_and_ignores_duplicates():
    engine = make_engine()
    df = sample_clean_df()
    load.load_dimension_tables(df, engine)

    load.load_price_observations(df, engine)
    load.load_price_observations(df, engine)

    assert scalar(engine, "SELECT COUNT(*) FROM crypto_price_observations") == 2
