"""extract_metadata_fields_into_columns

Extracts commonly-used fields from metadata_json into dedicated columns:
- lyrics (Στίχοι) - Critical for game content
- recording_date (Χρονολογία ηχογράφησης) - For era classification
- matrix_number (Αριθμός μήτρας) - Catalog reference
- dance_rhythm (Χορός / Ρυθμός) - For gameplay mechanics
- singers (Τραγουδιστές) - Artist information
- duration (Διάρκεια) - Track length
- recording_place (Τόπος ηχογράφησης) - Geographic data

Revision ID: d5b976a1f66e
Revises:
Create Date: 2026-01-01 16:09:25.828126

"""

import json
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5b976a1f66e"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add columns and extract metadata from JSON."""
    # Step 1: Add new columns to items table
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.add_column(sa.Column("lyrics", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("recording_date", sa.String(50), nullable=True))
        batch_op.add_column(sa.Column("matrix_number", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("dance_rhythm", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("singers", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("duration", sa.String(20), nullable=True))
        batch_op.add_column(sa.Column("recording_place", sa.String(200), nullable=True))

    # Step 2: Extract data from metadata_json
    conn = op.get_bind()
    items = conn.execute(sa.text("SELECT id, metadata_json FROM items")).fetchall()

    field_mapping = {
        "lyrics": "Στίχοι",
        "recording_date": "Χρονολογία ηχογράφησης",
        "matrix_number": "Αριθμός μήτρας",
        "dance_rhythm": "Χορός / Ρυθμός",
        "singers": "Τραγουδιστές",
        "duration": "Διάρκεια",
        "recording_place": "Τόπος ηχογράφησης",
    }

    for item_id, metadata_json in items:
        if not metadata_json:
            continue

        try:
            metadata = json.loads(metadata_json)
            updates = {}

            for col_name, json_key in field_mapping.items():
                if json_key in metadata and metadata[json_key]:
                    updates[col_name] = metadata[json_key]

            if updates:
                # Build UPDATE statement dynamically
                set_clause = ", ".join(f"{k} = :{k}" for k in updates)
                query = f"UPDATE items SET {set_clause} WHERE id = :id"
                updates["id"] = item_id
                conn.execute(sa.text(query), updates)

        except json.JSONDecodeError:
            # Skip malformed JSON
            continue

    # Step 3: Create indexes for common queries
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.create_index("ix_items_recording_date", ["recording_date"])
        batch_op.create_index("ix_items_dance_rhythm", ["dance_rhythm"])


def downgrade() -> None:
    """Remove extracted columns (data loss on downgrade)."""
    with op.batch_alter_table("items", schema=None) as batch_op:
        # Drop indexes
        batch_op.drop_index("ix_items_dance_rhythm")
        batch_op.drop_index("ix_items_recording_date")

        # Drop columns
        batch_op.drop_column("recording_place")
        batch_op.drop_column("duration")
        batch_op.drop_column("singers")
        batch_op.drop_column("dance_rhythm")
        batch_op.drop_column("matrix_number")
        batch_op.drop_column("recording_date")
        batch_op.drop_column("lyrics")
