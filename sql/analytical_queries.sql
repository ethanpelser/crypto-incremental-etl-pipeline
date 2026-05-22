-- Latest price for each coin
SELECT
    c.coin_id,
    c.coin_name,
    cur.currency_code,
    MAX(o.price_timestamp),
    ROUND(o.price, 2) AS latest_price
FROM crypto_price_observations o
JOIN coins c ON o.coin_key = c.coin_key
JOIN currencies cur ON o.currency_key = cur.currency_key
WHERE o.price_timestamp = (
    SELECT MAX(o2.price_timestamp)
    FROM crypto_price_observations o2
    WHERE o2.coin_key = o.coin_key
        AND o2.currency_key = o.currency_key
);

-- Average price by coin
SELECT 
    c.coin_id,
    c.coin_name,
    ROUND(AVG(o.price), 2) AS average_price
    FROM crypto_price_observations o
    JOIN coins c ON o.coin_key = c.coin_key
    GROUP BY c.coin_id, c.coin_name
    ORDER BY average_price DESC;

-- Highest price by coin
SELECT
    c.coin_id,
    c.coin_name,
    MAX(o.price) AS highest_price
FROM crypto_price_observations o
JOIN coins c ON o.coin_key = c.coin_key
GROUP BY c.coin_id, c.coin_name
ORDER BY highest_price DESC;

-- Lowest price by coin

SELECT 
    c.coin_id,
    c.coin_name,
    MIN(o.price) AS lowest_price
FROM crypto_price_observations o
JOIN coins c ON o.coin_key = c.coin_key
GROUP BY c.coin_id, c.coin_name
ORDER BY lowest_price DESC;

-- Average trading volume by coin

SELECT 
    c.coin_id,
    c.coin_name,
    ROUND(AVG(o.total_volume), 2) AS average_volume
    FROM crypto_price_observations o
    JOIN coins c ON o.coin_key = c.coin_key
    GROUP BY coin_name, coin_id
    ORDER BY average_volume DESC;

-- Daily average price by coin
SELECT 
    c.coin_id,
    c.coin_name,
    DATE(o.price_timestamp) AS price_date,
    ROUND(AVG(o.price), 2) AS average_price
FROM crypto_price_observations o
JOIN coins c ON o.coin_key = c.coin_key
GROUP BY c.coin_id, c.coin_name, price_date
ORDER BY price_date, coin_id;

-- Daily average volume by coin
SELECT 
    c.coin_id,
    c.coin_name,
    DATE(o.price_timestamp) AS price_date,
    ROUND(AVG(o.total_volume), 2) as daily_average_volume
FROM crypto_price_observations o
JOIN coins c ON o.coin_key = c.coin_key
GROUP BY coin_id, coin_name, DATE(o.price_timestamp)
ORDER BY coin_id, price_date;

-- Price change from earliest to latest  records
SELECT
    c.coin_id,
    c.coin_name,
    ROUND(first_price.price, 2) as initial_price,
    ROUND(last_price.price, 2) as final_price,
    ROUND(last_price.price - first_price.price, 2) as price_change,
    ROUND(((last_price.price - first_price.price)/first_price.price) *100, 2) as percent_change
FROM coins c
JOIN crypto_price_observations first_price
    ON c.coin_key = first_price.coin_key
JOIN crypto_price_observations last_price
    On c.coin_key = last_price.coin_key
WHERE first_price.price_timestamp = (
    SELECT 
    MIN(o.price_timestamp) 
    FROM crypto_price_observations o
    WHERE o.coin_key = c.coin_key
)
AND
    last_price.price_timestamp = (
    SELECT
    MAX(o.price_timestamp) 
    FROM crypto_price_observations o
    WHERE o.coin_key = c.coin_key
);


    