CREATE TABLE IF NOT EXISTS coins(
coin_key INTEGER PRIMARY KEY AUTOINCREMENT,
coin_id TEXT NOT NULL UNIQUE,
coin_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS currencies(
    currency_key INTEGER PRIMARY KEY AUTOINCREMENT,
    currency_code TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS crypto_prices_observations(
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

    UNIQUE (observation_id, currency_key, coin_key)
);
