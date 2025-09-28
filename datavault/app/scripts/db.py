from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg.rows import dict_row

from .config import DbConfig


@contextmanager
def get_conn(cfg: DbConfig) -> Iterator[psycopg.Connection]:
    conn = psycopg.connect(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
        dbname=cfg.dbname,
        autocommit=True,
        row_factory=dict_row,
    )
    try:
        yield conn
    finally:
        conn.close()


def exec_sql(conn: psycopg.Connection, sql: str, params: tuple | None = None) -> None:
    with conn.cursor() as cur:
        cur.execute(sql, params)


def fetch_all(conn: psycopg.Connection, sql: str, params: tuple | None = None):
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

