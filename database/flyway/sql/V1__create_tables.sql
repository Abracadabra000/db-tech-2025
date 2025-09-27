CREATE TABLE IF NOT EXISTS customer (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    rowguid         UUID NOT NULL DEFAULT gen_random_uuid(),
    modified_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS category (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    rowguid         UUID NOT NULL DEFAULT gen_random_uuid(),
    modified_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS product (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    catalog_price   FLOAT NOT NULL CHECK (catalog_price > 0),
    rowguid         UUID NOT NULL DEFAULT gen_random_uuid(),
    modified_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS product_category (
    id              SERIAL PRIMARY KEY,
    product_id      INTEGER NOT NULL,
    category_id     INTEGER NOT NULL,
    rowguid         UUID NOT NULL DEFAULT gen_random_uuid(),
    modified_date   TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_product_category UNIQUE (product_id, category_id)
);

CREATE TABLE IF NOT EXISTS deal (
    id              SERIAL PRIMARY KEY,
    customer_id     INTEGER NOT NULL,
    deal_date       TIMESTAMPTZ NOT NULL DEFAULT now(),
    total_amount    FLOAT NOT NULL DEFAULT 0,
    rowguid         UUID NOT NULL DEFAULT gen_random_uuid(),
    modified_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS deal_item (
    id              SERIAL PRIMARY KEY,
    deal_id         INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    price           FLOAT NOT NULL CHECK (price >= 0),
    rowguid         UUID NOT NULL DEFAULT gen_random_uuid(),
    modified_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);

