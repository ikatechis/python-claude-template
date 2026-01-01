"""normalize_recording_place

Maps recording_place variations to canonical recording_places.
- Adds recording_place_id FK column
- Adds recording_place_uncertain BOOLEAN column
- Maps all variants, handling uncertainty markers
- Preserves original in recording_place_raw

Revision ID: 674c9d9d6bd1
Revises: 943070a6d1d8
Create Date: 2026-01-01 17:35:xx

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "674c9d9d6bd1"
down_revision: str | Sequence[str] | None = "943070a6d1d8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Normalize recording_place to recording_places lookup."""
    conn = op.get_bind()

    # Step 1: Add columns
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.add_column(sa.Column("recording_place_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("recording_place_uncertain", sa.Boolean(), nullable=True))

    # Step 2: Create mapping for clean values
    place_mappings = {
        "Αθήνα": 1,
        "Θεσσαλονίκη": 2,
        "Σμύρνη": 3,
        "Κωνσταντινούπολη": 4,
        "Κωσταντινούπολη": 4,  # Typo fix
        "Νέα Υόρκη": 5,
        "Σικάγο": 6,
        "ΗΠΑ": 7,
        "Κάμντεν, Νέα Υερσέη": 8,
        "Βερολίνο": 9,
        "Μιλάνο": 10,
        "Βιέννη": 11,
        "Λονδίνο": 12,
        "Παρίσι": 13,
        "Γερμανία": 14,
        "Ευρώπη": 15,
        "Γαλλία": 16,
        "Κάιρο": 17,
        "Αλεξάνδρεια": 18,
        "Βίλνα": 19,
    }

    # Step 3: Update clean values first
    for variant, place_id in place_mappings.items():
        conn.execute(
            sa.text(
                "UPDATE items SET recording_place_id = :place_id WHERE recording_place = :variant"
            ),
            {"place_id": place_id, "variant": variant},
        )

    # Step 4: Handle uncertain markers "(;)"
    uncertain_patterns = [
        ("Αθήνα (;)", 1),
        ("Κωνσταντινούπολη (;)", 4),
        ("Θεσσαλονίκη (;)", 2),
        ("Νέα Υόρκη (;)", 5),
        ("Βερολίνο (;)", 9),
        ("Μιλάνο (;)", 10),
        ("Σικάγο (;)", 6),
        ("Σικάγο(;)", 6),  # No space variant
        ("Κωσταντινούπολη (;)", 4),  # Typo variant
        ("Γαλλία (;)", 16),
    ]

    for variant, place_id in uncertain_patterns:
        conn.execute(
            sa.text(
                """
                UPDATE items
                SET recording_place_id = :place_id,
                    recording_place_uncertain = 1
                WHERE recording_place = :variant
            """
            ),
            {"place_id": place_id, "variant": variant},
        )

    # Step 5: Handle compound places (take first location)
    compound_patterns = [
        ("Αθήνα ή Σμύρνη", 1, True),  # Athens uncertain
        ("Κωνσταντινούπολη ή Βερολίνο", 4, True),
        ("Αθήνα ή Βερολίνο", 1, True),
    ]

    for variant, place_id, uncertain in compound_patterns:
        conn.execute(
            sa.text(
                """
                UPDATE items
                SET recording_place_id = :place_id,
                    recording_place_uncertain = :uncertain
                WHERE recording_place = :variant
            """
            ),
            {"place_id": place_id, "uncertain": 1 if uncertain else 0, "variant": variant},
        )

    # Step 6: Handle bare uncertainty markers
    conn.execute(
        sa.text("UPDATE items SET recording_place_uncertain = 1 WHERE recording_place = ';'")
    )

    # Step 7: Rename original column to _raw
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.alter_column(
            "recording_place",
            new_column_name="recording_place_raw",
            existing_type=sa.Text(),
        )

    # Step 8: Create index and FK
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.create_index("ix_items_recording_place_id", ["recording_place_id"])
        batch_op.create_index("ix_items_recording_place_uncertain", ["recording_place_uncertain"])
        batch_op.create_foreign_key(
            "fk_items_recording_place",
            "recording_places",
            ["recording_place_id"],
            ["id"],
        )


def downgrade() -> None:
    """Restore original recording_place column."""
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.drop_constraint("fk_items_recording_place", type_="foreignkey")
        batch_op.drop_index("ix_items_recording_place_uncertain")
        batch_op.drop_index("ix_items_recording_place_id")
        batch_op.alter_column(
            "recording_place_raw",
            new_column_name="recording_place",
            existing_type=sa.Text(),
        )
        batch_op.drop_column("recording_place_uncertain")
        batch_op.drop_column("recording_place_id")
