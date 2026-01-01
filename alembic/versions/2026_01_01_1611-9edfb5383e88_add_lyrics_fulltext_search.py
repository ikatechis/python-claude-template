"""add_lyrics_fulltext_search

Creates FTS5 virtual table for full-text search across:
- lyrics (Στίχοι) - Primary search field
- title - Song titles
- first_words - Opening lyrics
- creator_composer - Artist names

This enables efficient semantic search for the RAG pipeline and in-game search.

Revision ID: 9edfb5383e88
Revises: d5b976a1f66e
Create Date: 2026-01-01 16:11:18.062339

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9edfb5383e88"
down_revision: str | Sequence[str] | None = "d5b976a1f66e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create FTS5 virtual table for lyrics and content search."""
    conn = op.get_bind()

    # Create FTS5 virtual table
    conn.execute(
        sa.text(
            """
        CREATE VIRTUAL TABLE items_fts USING fts5(
            id UNINDEXED,
            title,
            lyrics,
            first_words,
            creator_composer,
            content='items',
            content_rowid='rowid'
        )
    """
        )
    )

    # Populate FTS table with existing data
    conn.execute(
        sa.text(
            """
        INSERT INTO items_fts(rowid, id, title, lyrics, first_words, creator_composer)
        SELECT rowid, id, title, lyrics, first_words, creator_composer
        FROM items
    """
        )
    )

    # Create triggers to keep FTS table in sync with items table
    # Trigger for INSERT
    conn.execute(
        sa.text(
            """
        CREATE TRIGGER items_ai AFTER INSERT ON items BEGIN
            INSERT INTO items_fts(rowid, id, title, lyrics, first_words, creator_composer)
            VALUES (new.rowid, new.id, new.title, new.lyrics, new.first_words, new.creator_composer);
        END
    """
        )
    )

    # Trigger for DELETE
    conn.execute(
        sa.text(
            """
        CREATE TRIGGER items_ad AFTER DELETE ON items BEGIN
            DELETE FROM items_fts WHERE rowid = old.rowid;
        END
    """
        )
    )

    # Trigger for UPDATE
    conn.execute(
        sa.text(
            """
        CREATE TRIGGER items_au AFTER UPDATE ON items BEGIN
            DELETE FROM items_fts WHERE rowid = old.rowid;
            INSERT INTO items_fts(rowid, id, title, lyrics, first_words, creator_composer)
            VALUES (new.rowid, new.id, new.title, new.lyrics, new.first_words, new.creator_composer);
        END
    """
        )
    )


def downgrade() -> None:
    """Remove FTS table and triggers."""
    conn = op.get_bind()

    # Drop triggers
    conn.execute(sa.text("DROP TRIGGER IF EXISTS items_au"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS items_ad"))
    conn.execute(sa.text("DROP TRIGGER IF EXISTS items_ai"))

    # Drop FTS table
    conn.execute(sa.text("DROP TABLE IF EXISTS items_fts"))
