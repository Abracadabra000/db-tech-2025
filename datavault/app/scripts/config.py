import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    dbname: str


def load_db_config_from_env() -> DbConfig:
    return DbConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        user=os.getenv("DB_USER", "app"),
        password=os.getenv("DB_PASSWORD", "app"),
        dbname=os.getenv("DB_NAME", "dv"),
    )


def get_seed_count() -> int:
    try:
        return max(1, int(os.getenv("SEED_COUNT", "25")))
    except ValueError:
        return 25

