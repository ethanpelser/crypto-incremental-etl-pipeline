-- count total coins
SELECT COUNT(*) AS coin_count
FROM coins;

-- count total currencies
SELECT COUNT(*) AS currency_count
FROM currencies;

-- count total price observations
SELECT COUNT(*) AS observation_count
FROM crypto_price_observations;

-- Count observatins by coin
SELECT 
    c.coin_id,
    COUNT(*) AS observation_count
FROM crypto_price_observations o
JOIN coins c ON o.coin_key = c.coin_key
GROUP BY c.coin_id;

-- check duplicate price observations
SELECT
    coin_key,
    currency_key,
    price_timestamp,
    COUNT(*) AS duplicate_count
FROM crypto_price_observations
GROUP BY coin_key, currency_key, price_timestamp
HAVING COUNT(*) > 1;

-- Check missing require values
SELECT * 
FROM crypto_price_observations
WHERE coin_key IS NULL
    OR currency_key IS NULL
    OR price_timestamp IS NULL
    OR price IS NULL;

-- Check invalid prices
SELECT *
FROM crypto_price_observations
WHERE price <= 0;

-- Check orphaned coin foreign keys
SELECT *
FROM crypto_price_observations o
JOIN coins c ON o.coin_key = c.coin_key
WHERE c.coin_key IS NULL;

-- Check for orphaned curreny foreign keys
SELECT *
FROM crypto_price_observations o 
JOIN currencies c ON o.currency_key = c.currency_key
WHERE c.currency_key IS NULL;
    