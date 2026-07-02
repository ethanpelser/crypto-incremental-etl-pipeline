import sqlite3
from pathlib import Path

import create_database


def test_create_database_creates_expected_tables(tmp_path, monkeypatch):
    db_path = tmp_path / "test_crypto_prices.db"
    sql_file = tmp_path / "create_tables.sql"
    sql_file.write_text(
        """
        CREATE TABLE coins(coin_key INTEGER PRIMARY KEY, coin_id TEXT, coin_name TEXT);
        CREATE TABLE currencies(currency_key INTEGER PRIMARY KEY, currency_code TEXT);
        CREATE TABLE crypto_price_observations(observation_id INTEGER PRIMARY KEY, price REAL);
        """,
        encoding="utf-8",
    )
    monkeypatch.setattr(create_database, "DATABASE_PATH", str(db_path))
    monkeypatch.setattr(create_database, "SQL_FILE", str(sql_file))

    create_database.create_database()

    with sqlite3.connect(db_path) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

    assert {"coins", "currencies", "crypto_price_observations"}.issubset(tables)
