import json
from pathlib import Path

import pytest

import extract


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload
        self.raise_for_status_called = False

    def raise_for_status(self):
        self.raise_for_status_called = True

    def json(self):
        return self.payload


def test_extract_coin_data_calls_coingecko_with_expected_params(monkeypatch):
    payload = {"prices": [[1700000000000, 50000.0]]}
    response = DummyResponse(payload)
    captured = {}

    def fake_get(url, params, timeout):
        captured["url"] = url
        captured["params"] = params
        captured["timeout"] = timeout
        return response

    monkeypatch.setattr(extract.requests, "get", fake_get)

    result = extract.extract_coin_data("bitcoin")

    assert result == payload
    assert captured["url"] == "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    assert captured["params"] == {"vs_currency": "usd", "days": "7"}
    assert captured["timeout"] == 30
    assert response.raise_for_status_called is True


def test_save_raw_data_writes_json_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = {"prices": [[1700000000000, 50000.0]], "market_caps": [], "total_volumes": []}

    extract.save_raw_data(data, "bitcoin")

    output_file = Path("data/raw/bitcoin_raw.json")
    assert output_file.exists()
    assert json.loads(output_file.read_text(encoding="utf-8")) == data


def test_extract_all_coins_extracts_and_saves_each_configured_coin(monkeypatch):
    calls = []
    saved = []

    monkeypatch.setattr(extract, "COINS", {"bitcoin": "Bitcoin", "ethereum": "Ethereum"})

    def fake_extract_coin_data(coin_id):
        calls.append(coin_id)
        return {"coin": coin_id}

    def fake_save_raw_data(data, coin_id):
        saved.append((coin_id, data))

    monkeypatch.setattr(extract, "extract_coin_data", fake_extract_coin_data)
    monkeypatch.setattr(extract, "save_raw_data", fake_save_raw_data)

    extract.extract_all_coins()

    assert calls == ["bitcoin", "ethereum"]
    assert saved == [("bitcoin", {"coin": "bitcoin"}), ("ethereum", {"coin": "ethereum"})]
