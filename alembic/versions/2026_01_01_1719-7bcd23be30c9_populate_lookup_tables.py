"""populate_lookup_tables

Populates rhythm_types and recording_places with canonical values
based on data quality analysis from tools/analyze_data_quality.py

Revision ID: 7bcd23be30c9
Revises: 3664e06aa7e0
Create Date: 2026-01-01 17:19:36.376545

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7bcd23be30c9"
down_revision: str | Sequence[str] | None = "3664e06aa7e0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Populate lookup tables with canonical values."""
    conn = op.get_bind()

    # Populate rhythm_types
    # Data from analysis: Top rhythms found in database
    rhythms = [
        # Traditional Greek rhythms
        (1, "Ζεϊμπέκικος", "Zeibekiko", "traditional", "9/8", 1),
        (2, "Χασάπικος", "Hasapiko", "traditional", "2/4", 1),
        (3, "Τσιφτετέλι", "Tsifteteli", "traditional", "4/4", 1),
        (4, "Συρτός", "Syrtos", "traditional", "2/4", 1),
        (5, "Καρσιλαμάς", "Karsilamas", "traditional", "9/8", 1),
        (6, "Τσάμικος", "Tsamikos", "traditional", "3/4", 1),
        (7, "Καλαματιανός", "Kalamatiano", "traditional", "7/8", 1),
        (8, "Μπάλος", "Balos", "traditional", "3/4", 1),
        (9, "Σούστα", "Sousta", "traditional", "2/4", 1),
        # Western rhythms
        (10, "Ταγκό", "Tango", "western", "4/4", 1),
        (11, "Βαλς", "Waltz", "western", "3/4", 1),
        (12, "Φοξ", "Foxtrot", "western", "4/4", 1),
        (13, "Τσάρλεστον", "Charleston", "western", "4/4", 1),
        (14, "Ουάν στεπ", "One-step", "western", "2/4", 1),
        (15, "Ρούμπα", "Rumba", "western", "4/4", 1),
        (16, "Μπλουζ", "Blues", "western", "4/4", 1),
    ]

    for rhythm in rhythms:
        conn.execute(
            sa.text(
                """
                INSERT INTO rhythm_types (id, name_el, name_en, category, time_signature, game_relevant)
                VALUES (:id, :name_el, :name_en, :category, :time_signature, :game_relevant)
            """
            ),
            {
                "id": rhythm[0],
                "name_el": rhythm[1],
                "name_en": rhythm[2],
                "category": rhythm[3],
                "time_signature": rhythm[4],
                "game_relevant": rhythm[5],
            },
        )

    # Populate recording_places
    # Data from analysis: Top places found in database
    places = [
        # Greece
        (1, "Αθήνα", "Athens", "Greece", 37.9838, 23.7275),
        (2, "Θεσσαλονίκη", "Thessaloniki", "Greece", 40.6401, 22.9444),
        (3, "Σμύρνη", "Smyrna", "Turkey", 38.4237, 27.1428),
        # Turkey/Constantinople
        (4, "Κωνσταντινούπολη", "Constantinople", "Turkey", 41.0082, 28.9784),
        # USA
        (5, "Νέα Υόρκη", "New York", "USA", 40.7128, -74.0060),
        (6, "Σικάγο", "Chicago", "USA", 41.8781, -87.6298),
        (7, "ΗΠΑ", "USA", "USA", None, None),
        (8, "Κάμντεν, Νέα Υερσέη", "Camden, NJ", "USA", 39.9259, -75.1196),
        # Europe
        (9, "Βερολίνο", "Berlin", "Germany", 52.5200, 13.4050),
        (10, "Μιλάνο", "Milan", "Italy", 45.4642, 9.1900),
        (11, "Βιέννη", "Vienna", "Austria", 48.2082, 16.3738),
        (12, "Λονδίνο", "London", "UK", 51.5074, -0.1278),
        (13, "Παρίσι", "Paris", "France", 48.8566, 2.3522),
        (14, "Γερμανία", "Germany", "Germany", None, None),
        (15, "Ευρώπη", "Europe", None, None, None),
        (16, "Γαλλία", "France", "France", None, None),
        # Middle East/Africa
        (17, "Κάιρο", "Cairo", "Egypt", 30.0444, 31.2357),
        (18, "Αλεξάνδρεια", "Alexandria", "Egypt", 31.2001, 29.9187),
        # Eastern Europe
        (19, "Βίλνα", "Vilnius", "Lithuania", 54.6872, 25.2797),
    ]

    for place in places:
        conn.execute(
            sa.text(
                """
                INSERT INTO recording_places (id, name_el, name_en, country, latitude, longitude)
                VALUES (:id, :name_el, :name_en, :country, :latitude, :longitude)
            """
            ),
            {
                "id": place[0],
                "name_el": place[1],
                "name_en": place[2],
                "country": place[3],
                "latitude": place[4],
                "longitude": place[5],
            },
        )


def downgrade() -> None:
    """Clear lookup tables."""
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM recording_places"))
    conn.execute(sa.text("DELETE FROM rhythm_types"))
