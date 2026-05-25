# Crypto Incremental ETL Pipeline

## Overview

This project is a local incremental ETL pipeline that extracts cryptocurrency market data from the CoinGecko API, transforms the raw JSON response into clean tabular data, and loads it into a normalized SQLite database.

The main goal of this project is to demonstrate how an ETL pipeline can load only new records instead of deleting and reloading the full dataset every time.

This project demonstrates:

- API extraction
- JSON transformation
- Normalized database design
- Incremental loading
- Duplicate prevention
- Data validation
- Analytical SQL queries
- Modular Python pipeline design

---

## Technologies Used

- Python
- pandas
- requests
- SQLite
- SQLAlchemy
- SQL
- Git / GitHub

---

## API Source

Data is extracted from the CoinGecko API.

API documentation:

https://docs.coingecko.com/reference/introduction

The pipeline currently extracts market data for:

- Bitcoin
- Ethereum

---

## Pipeline Flow

```text
CoinGecko API
        ↓
Raw JSON files
        ↓
Cleaned CSV file
        ↓
Normalized SQLite database
        ↓
Validation checks
        ↓
Analytical SQL queries
```

---

## Project Structure

```text
crypto-incremental-etl-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── sql/
│   ├── create_tables.sql
│   ├── validation_checks.sql
│   └── analytical_queries.sql
│
├── src/
│   ├── create_database.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── validate.py
│   ├── run_analytics.py
│   └── pipeline.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Database Design

The project uses a normalized SQLite database.

### `coins`

Stores unique cryptocurrency information.

| Column | Description |
|---|---|
| `coin_key` | Primary key |
| `coin_id` | CoinGecko coin ID, such as `bitcoin` |
| `coin_name` | Readable coin name, such as `Bitcoin` |

### `currencies`

Stores unique currency codes.

| Column | Description |
|---|---|
| `currency_key` | Primary key |
| `currency_code` | Currency code, such as `usd` |

### `crypto_price_observations`

Stores timestamped cryptocurrency market observations.

| Column | Description |
|---|---|
| `observation_id` | Primary key |
| `coin_key` | Foreign key to `coins` |
| `currency_key` | Foreign key to `currencies` |
| `price_timestamp` | Timestamp of the market observation |
| `price` | Cryptocurrency price |
| `market_cap` | Market capitalization |
| `total_volume` | Trading volume |
| `loaded_at` | Time the record was loaded into the database |

---

## Incremental Loading

The pipeline uses a unique constraint on:

```sql
coin_key, currency_key, price_timestamp
```

This prevents the same cryptocurrency observation from being inserted more than once.

The loading script uses:

```sql
INSERT OR IGNORE
```

This means:

```text
new records are inserted
existing records are skipped
```

If the pipeline is run twice with the same source data, the second run should load:

```text
0 new price observations
```

---

## How to Run the Project

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

Git Bash:

```bash
source venv/Scripts/activate
```

Windows CMD:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the full pipeline

```bash
py src/pipeline.py
```

The pipeline will:

1. Create the SQLite database and tables
2. Extract cryptocurrency data from the CoinGecko API
3. Save raw JSON files
4. Transform raw JSON into a cleaned CSV
5. Load only new records into the normalized database
6. Run validation checks

---

## Run Individual Steps

Create the database:

```bash
py src/create_database.py
```

Extract raw data:

```bash
py src/extract.py
```

Transform raw JSON into CSV:

```bash
py src/transform.py
```

Load data incrementally:

```bash
py src/load.py
```

Run validation checks:

```bash
py src/validate.py
```

Run analytical queries:

```bash
py src/run_analytics.py
```

---

## Validation Checks

The project includes SQL validation checks for:

- total row counts
- duplicate price observations
- missing required values
- invalid prices
- orphaned foreign keys
- observations by coin

Validation checks are stored in:

```text
sql/validation_checks.sql
```

---

## Analytical Queries

The project includes analytical SQL queries for:

- latest price by coin
- average price by coin
- highest price by coin
- lowest price by coin
- daily average price
- daily average trading volume
- price change from earliest to latest record

Analytical queries are stored in:

```text
sql/analytical_queries.sql
```

---

## Key Design Decisions

- Raw API responses are saved as JSON for debugging and reproducibility.
- Cleaned data is saved as CSV before loading into the database.
- The database is normalized into separate coin, currency, and observation tables.
- Incremental loading prevents duplicate observations.
- Validation checks are included to verify data quality.
- Analytical SQL queries demonstrate how the loaded data can be used for reporting.

---

## Future Improvements

Possible future improvements:

- Add more cryptocurrencies
- Add more currencies
- Add logging
- Add unit tests
- Add PostgreSQL support
- Add scheduled pipeline runs
- Add dashboard visualizations
- Add better API error handling and retry logic

---