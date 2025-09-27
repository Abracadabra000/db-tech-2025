from random import randint, sample, uniform

from faker import Faker
from rich import print

from .config import load_db_config_from_env, get_seed_count
from .db import get_conn, exec_sql, fetch_all


fake = Faker()


def ensure_min_counts(conn):
    base_count = get_seed_count()
    # ensure 25 rows for base entities and 50+ for linking entities
    # customers
    customers = fetch_all(conn, "SELECT id FROM customer")
    to_add = max(0, base_count - len(customers))
    for _ in range(to_add):
        exec_sql(conn, "INSERT INTO customer(name) VALUES (%s) ON CONFLICT DO NOTHING", (fake.unique.company(),))

    # categories
    categories = fetch_all(conn, "SELECT id FROM category")
    to_add = max(0, base_count - len(categories))
    for _ in range(to_add):
        exec_sql(conn, "INSERT INTO category(name) VALUES (%s) ON CONFLICT DO NOTHING", (fake.unique.word().title(),))

    # products
    products = fetch_all(conn, "SELECT id FROM product")
    to_add = max(0, base_count - len(products))
    for _ in range(to_add):
        price = round(uniform(5, 500), 2)
        exec_sql(conn, "INSERT INTO product(name, catalog_price) VALUES (%s, %s)", (fake.unique.catch_phrase(), price))

    # product-category links: aim for >= 50
    products = fetch_all(conn, "SELECT id FROM product")
    categories = fetch_all(conn, "SELECT id FROM category")
    existing_links = fetch_all(conn, "SELECT product_id, category_id FROM product_category")
    existing_set = {(r["product_id"], r["category_id"]) for r in existing_links}
    target_links = max(base_count * 2, len(products) * 2)
    while len(existing_set) < target_links and products and categories:
        p = sample(products, 1)[0]["id"]
        c = sample(categories, 1)[0]["id"]
        if (p, c) not in existing_set:
            exec_sql(conn, "INSERT INTO product_category(product_id, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (p, c))
            existing_set.add((p, c))

    # deals and deal_items
    customers = fetch_all(conn, "SELECT id FROM customer")
    products = fetch_all(conn, "SELECT id, catalog_price FROM product")
    # create at least 25 deals
    deal_ids = []
    deals_to_create = max(0, base_count - len(fetch_all(conn, "SELECT id FROM deal")))
    for _ in range(deals_to_create):
        cust = sample(customers, 1)[0]["id"]
        exec_sql(conn, "INSERT INTO deal(customer_id) VALUES (%s)", (cust,))
    deal_ids = [r["id"] for r in fetch_all(conn, "SELECT id FROM deal")] 

    # ensure at least 50 deal items
    existing_items = fetch_all(conn, "SELECT id FROM deal_item")
    to_create = max(0, base_count * 2 - len(existing_items))
    for _ in range(to_create):
        deal_id = sample(deal_ids, 1)[0]
        product = sample(products, 1)[0]
        quantity = randint(1, 10)
        # price can differ from catalog price by +/-20%
        base_price = float(product["catalog_price"])  # works for both NUMERIC and FLOAT columns
        multiplier = uniform(0.8, 1.2)
        price = round(base_price * multiplier, 2)
        exec_sql(
            conn,
            "INSERT INTO deal_item(deal_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (deal_id, product["id"], quantity, price),
        )


def seed_current_db():
    from psycopg.errors import UndefinedTable

    with get_conn(load_db_config_from_env()) as conn:
        try:
            ensure_min_counts(conn)
        except UndefinedTable:
            raise RuntimeError("Schema not found. Run Flyway migrations first.")


def main():
    print("[cyan]Seeding current DB...")
    seed_current_db()
    print("[green]Seeding complete")


if __name__ == "__main__":
    main()

