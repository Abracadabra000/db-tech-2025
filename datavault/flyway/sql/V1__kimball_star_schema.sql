CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key     SERIAL PRIMARY KEY,
    customer_name    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_key      SERIAL PRIMARY KEY,
    product_name     TEXT NOT NULL,
    catalog_price    FLOAT NOT NULL CHECK (catalog_price > 0)
);

CREATE TABLE IF NOT EXISTS dim_product_category (
    product_category_key SERIAL PRIMARY KEY,
    product_category_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_product_category_link (
    product_category_link_key SERIAL PRIMARY KEY,
    product_key BIGINT NOT NULL,
    product_category_key BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key         BIGSERIAL PRIMARY KEY,
    year             INTEGER NOT NULL,
    month            INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    day              INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    hour             INTEGER NOT NULL CHECK (hour BETWEEN 0 AND 23),
    minute           INTEGER NOT NULL CHECK (minute BETWEEN 0 AND 59),
    second           INTEGER NOT NULL CHECK (second BETWEEN 0 AND 59)
);

CREATE TABLE IF NOT EXISTS dim_deal_item (
    deal_item_key    BIGSERIAL PRIMARY KEY,
    deal_key         BIGINT NOT NULL,
    product_key      BIGINT NOT NULL,
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    total_price     FLOAT NOT NULL CHECK (total_price >= 0)
);

CREATE TABLE IF NOT EXISTS deal_fact (
    deal_key         BIGSERIAL PRIMARY KEY, 
    customer_key     BIGINT NOT NULL,
    date_key         BIGINT NOT NULL,
    total_price      FLOAT NOT NULL CHECK (total_price >= 0)
);

