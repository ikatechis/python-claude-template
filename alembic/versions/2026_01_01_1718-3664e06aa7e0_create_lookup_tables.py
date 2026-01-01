"""create_lookup_tables

Creates lookup tables for data normalization:
- rhythm_types: Canonical dance/rhythm values
- recording_places: Canonical recording locations

These tables will be populated in the next migration.

Revision ID: 3664e06aa7e0
Revises: 9edfb5383e88
Create Date: 2026-01-01 17:18:xx

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3664e06aa7e0"
down_revision: str | Sequence[str] | None = "9edfb5383e88"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create lookup tables for normalization."""
    # Create rhythm_types table
    op.create_table(
        "rhythm_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name_el", sa.Text(), nullable=False),
        sa.Column("name_en", sa.String(100), nullable=True),
        sa.Column(
            "category",
            sa.String(50),
            nullable=True,
            comment="traditional, urban, or western",
        ),
        sa.Column("time_signature", sa.String(10), nullable=True),
        sa.Column("game_relevant", sa.Boolean(), nullable=False, server_default="1"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name_el"),
    )

    # Create recording_places table
    op.create_table(
        "recording_places",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name_el", sa.Text(), nullable=False),
        sa.Column("name_en", sa.String(100), nullable=True),
        sa.Column("country", sa.String(100), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name_el"),
    )


def downgrade() -> None:
    """Drop lookup tables."""
    op.drop_table("recording_places")
    op.drop_table("rhythm_types")
