from random import randint, sample, uniform
from datetime import datetime, timedelta

from faker import Faker
from rich import print

from .config import load_db_config_from_env, get_seed_count
from .db import get_conn, exec_sql, fetch_all


fake = Faker()


def ensure_dims(conn, n):
    # customers
    customers = fetch_all(conn, "SELECT customer_key FROM dim_customer")
    for _ in range(max(0, n - len(customers))):
        exec_sql(conn, "INSERT INTO dim_customer(customer_name) VALUES (%s)", (fake.unique.company(),))

    # products
    products = fetch_all(conn, "SELECT product_key FROM dim_product")
    for _ in range(max(0, n - len(products))):
        exec_sql(conn, "INSERT INTO dim_product(product_name, catalog_price) VALUES (%s, %s)", (fake.unique.catch_phrase(), round(uniform(5, 500), 2)))

    # product categories
    categories = fetch_all(conn, "SELECT product_category_key FROM dim_product_category")
    to_add = max(0, n - len(categories))
    for _ in range(to_add):
        exec_sql(conn, "INSERT INTO dim_product_category(product_category_name) VALUES (%s)", (fake.unique.word().title(),))

    # link products to 1-2 categories
    products = fetch_all(conn, "SELECT product_key FROM dim_product")
    categories = fetch_all(conn, "SELECT product_category_key FROM dim_product_category")
    existing = fetch_all(conn, "SELECT product_key, product_category_key FROM dim_product_category_link")
    existing_set = {(r["product_key"], r["product_category_key"]) for r in existing}
    for p in products:
        for _ in range(randint(1, 2)):
            cat = sample(categories, 1)[0]["product_category_key"]
            pair = (p["product_key"], cat)
            if pair in existing_set:
                continue
            exec_sql(conn, "INSERT INTO dim_product_category_link(product_key, product_category_key) VALUES (%s, %s)", pair)
            existing_set.add(pair)

    # ensure some date-time rows exist (recent ~ 90 days, random times)
    dates_count = fetch_all(conn, "SELECT COUNT(*) AS c FROM dim_date")[0]["c"]
    target = max(n * 5, 90)  # enough for facts
    to_insert = max(0, target - dates_count)
    base = datetime.utcnow() - timedelta(days=90)
    for i in range(to_insert):
        dt = base + timedelta(minutes=randint(0, 90*24*60))
        exec_sql(
            conn,
            "INSERT INTO dim_date(year, month, day, hour, minute, second) VALUES (%s, %s, %s, %s, %s, %s)",
            (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second),
        )


def ensure_facts(conn, n):
    customers = [r["customer_key"] for r in fetch_all(conn, "SELECT customer_key FROM dim_customer")]
    products = fetch_all(conn, "SELECT product_key, catalog_price FROM dim_product")
    dates = [r["date_key"] for r in fetch_all(conn, "SELECT date_key FROM dim_date ORDER BY date_key DESC LIMIT 500")]

    # create ~ n deals
    existing_deals = fetch_all(conn, "SELECT COUNT(*) AS c FROM deal_fact")[0]["c"]
    deals_to_create = max(0, n - existing_deals)
    for _ in range(deals_to_create):
        customer_key = sample(customers, 1)[0]
        date_key = sample(dates, 1)[0]
        # create deal with zero, then add items and update total
        deal_row = fetch_all(conn, "INSERT INTO deal_fact(customer_key, date_key, total_price) VALUES (%s, %s, %s) RETURNING deal_key", (customer_key, date_key, 0.0))
        deal_key = deal_row[0]["deal_key"]

        items = randint(1, 5)
        running_total = 0.0
        for _i in range(items):
            product = sample(products, 1)[0]
            qty = randint(1, 10)
            total_price = round(qty * float(product["catalog_price"]), 2)
            running_total += total_price
            exec_sql(
                conn,
                "INSERT INTO dim_deal_item(deal_key, product_key, quantity, total_price) VALUES (%s, %s, %s, %s)",
                (deal_key, product["product_key"], qty, total_price),
            )
        exec_sql(conn, "UPDATE deal_fact SET total_price=%s WHERE deal_key=%s", (round(running_total, 2), deal_key))


def main():
    n = get_seed_count()
    with get_conn(load_db_config_from_env()) as conn:
        ensure_dims(conn, n)
        ensure_facts(conn, n)
    print("[green]Kimball seeding complete")


if __name__ == "__main__":
    main()

