#!/usr/bin/env python3
"""Quick SQLite query tool for Kounadis database."""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "vmrebetiko_all_genres.db"


def query(sql: str, limit: int = 10):
    """Execute SQL query and print results."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        if not rows:
            print("No results")
            return

        # Print column names
        cols = rows[0].keys()
        print(" | ".join(cols))
        print("-" * 80)

        # Print rows
        for row in rows[:limit]:
            print(" | ".join(str(row[col])[:30] for col in cols))

        if len(rows) > limit:
            print(f"\n... {len(rows) - limit} more rows")

        print(f"\nTotal: {len(rows)} rows")

    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def list_tables():
    """List all tables in the database."""
    query("SELECT name FROM sqlite_master WHERE type='table'")


def show_schema(table: str):
    """Show schema for a table."""
    query(f"PRAGMA table_info({table})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tools/query_db.py 'SELECT * FROM items LIMIT 5'")
        print("  python tools/query_db.py --tables")
        print("  python tools/query_db.py --schema items")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--tables":
        list_tables()
    elif arg == "--schema" and len(sys.argv) > 2:
        show_schema(sys.argv[2])
    else:
        query(arg)
