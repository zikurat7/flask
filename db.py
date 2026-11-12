import os

import psycopg
from psycopg.rows import dict_row


def get_db():
    """Open a PostgreSQL connection that returns rows as dicts."""
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)
