import json
from pathlib import Path

import pandas as pd

import transform


def write_raw_coin(tmp_path, coin_id, payload):
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_file = raw_dir / f"{coin_id}_raw.json"
    raw_file.write_text(json.dumps(payload), encoding="utf-8")
    return raw_file


def sample_payload():
    return {
        "prices": [
            [1700000000000, 50000.0],
            [1700000000000, 50000.0],  # duplicate timestamp should be dropped
            [1700003600000, 50100.0],
        ],
        "market_caps": [
            [1700000000000, 900000000.0],
            [1700000000000, 900000000.0],
            [1700003600000, 910000000.0],
        ],
        "total_volumes": [
            [1700000000000, 30000000.0],
            [1700000000000, 30000000.0],
            [1700003600000, 31000000.0],
        ],
    }


def test_transform_coin_data_returns_cleaned_dataframe(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_raw_coin(tmp_path, "bitcoin", sample_payload())

    df = transform.transform_coin_data("bitcoin", "Bitcoin")

    assert list(df.columns) == [
        "coin_id",
        "coin_name",
        "currency_code",
        "price_timestamp",
        "price",
        "market_cap",
        "total_volume",
    ]
    assert len(df) == 2
    assert df["coin_id"].tolist() == ["bitcoin", "bitcoin"]
    assert df["coin_name"].tolist() == ["Bitcoin", "Bitcoin"]
    assert df["currency_code"].tolist() == ["usd", "usd"]
    assert df["price"].tolist() == [50000.0, 50100.0]
    assert df.duplicated(subset=["coin_id", "currency_code", "price_timestamp"]).sum() == 0


def test_transform_all_coins_combines_all_coins_and_writes_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_raw_coin(tmp_path, "bitcoin", sample_payload())
    write_raw_coin(tmp_path, "ethereum", sample_payload())
    monkeypatch.setattr(transform, "COINS", {"bitcoin": "Bitcoin", "ethereum": "Ethereum"})

    final_df = transform.transform_all_coins()

    output_file = Path("data/processed/crypto_prices_cleaned.csv")
    assert output_file.exists()
    saved_df = pd.read_csv(output_file)
    assert len(final_df) == 4
    assert len(saved_df) == 4
    assert set(saved_df["coin_id"]) == {"bitcoin", "ethereum"}
