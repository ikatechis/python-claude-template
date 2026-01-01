"""normalize_dance_rhythm

Maps dance_rhythm variations to canonical rhythm_types.
- Adds rhythm_type_id FK column
- Maps all variants to canonical forms
- Preserves original in dance_rhythm_raw

Revision ID: 943070a6d1d8
Revises: 7bcd23be30c9
Create Date: 2026-01-01 17:29:xx

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "943070a6d1d8"
down_revision: str | Sequence[str] | None = "7bcd23be30c9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Normalize dance_rhythm to rhythm_types lookup."""
    conn = op.get_bind()

    # Step 1: Add rhythm_type_id column
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.add_column(sa.Column("rhythm_type_id", sa.Integer(), nullable=True))

    # Step 2: Create mapping from variants to canonical rhythm_type IDs
    # Based on data quality analysis
    rhythm_mappings = {
        # Ζεϊμπέκικος (id=1)
        "Ζεϊμπέκικος": 1,
        "Ζεϊμπέκικος [Απτάλικος]": 1,
        "Ζεϊμπέκικος [απτάλικος]": 1,
        # Χασάπικος (id=2)
        "Χασάπικος": 2,
        "Χασάπικο": 2,
        "Συρτός [Χασάπικος]": 2,  # Compound, use primary rhythm
        # Τσιφτετέλι (id=3)
        "Τσιφτετέλι": 3,
        # Συρτός (id=4)
        "Συρτός": 4,
        # Καρσιλαμάς (id=5)
        "Καρσιλαμάς": 5,
        "Καρσιλαμάς Πολίτικος": 5,
        # Τσάμικος (id=6)
        "Τσάμικος": 6,
        # Καλαματιανός (id=7)
        "Καλαματιανός": 7,
        "Καλαματιανό": 7,
        # Μπάλος (id=8)
        "Μπάλος": 8,
        # Σούστα (id=9)
        "Σούστα": 9,
        # Ταγκό (id=10)
        "Ταγκό": 10,
        # Βαλς (id=11)
        "Βαλς": 11,
        "[Βαλς]": 11,
        "Waltz": 11,
        # Φοξ (id=12) - All foxtrot variations
        "Φοξ": 12,
        "Φοξ τροτ": 12,
        "Φοξ-τροτ": 12,
        "Φοξ-Τροτ": 12,
        "Φοξ αργό": 12,
        "Σλόου φοξ": 12,
        "Fox-trot": 12,
        "Foxtrot": 12,
        # Τσάρλεστον (id=13)
        "Τσάρλεστον": 13,
        # Ουάν στεπ (id=14)
        "Ουάν στεπ": 14,
        "One step": 14,
        # Ρούμπα (id=15)
        "Ρούμπα": 15,
        # Μπλουζ (id=16)
        "Μπλουζ": 16,
        "Shimmy-blues": 16,
    }

    # Step 3: Update rhythm_type_id for all mapped values
    for variant, rhythm_id in rhythm_mappings.items():
        conn.execute(
            sa.text("UPDATE items SET rhythm_type_id = :rhythm_id WHERE dance_rhythm = :variant"),
            {"rhythm_id": rhythm_id, "variant": variant},
        )

    # Step 4: Rename original column to _raw (preserve unmapped values)
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.alter_column(
            "dance_rhythm", new_column_name="dance_rhythm_raw", existing_type=sa.Text()
        )

    # Step 5: Create index on rhythm_type_id for efficient filtering
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.create_index("ix_items_rhythm_type_id", ["rhythm_type_id"])
        batch_op.create_foreign_key(
            "fk_items_rhythm_type", "rhythm_types", ["rhythm_type_id"], ["id"]
        )


def downgrade() -> None:
    """Restore original dance_rhythm column."""
    with op.batch_alter_table("items", schema=None) as batch_op:
        batch_op.drop_constraint("fk_items_rhythm_type", type_="foreignkey")
        batch_op.drop_index("ix_items_rhythm_type_id")
        batch_op.alter_column(
            "dance_rhythm_raw", new_column_name="dance_rhythm", existing_type=sa.Text()
        )
        batch_op.drop_column("rhythm_type_id")
