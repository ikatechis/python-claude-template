---
status: stable
version: 1.0.0
last_updated: 2026-01-01
---

# Database Migrations with Alembic

This project uses **Alembic** for version-controlled database schema migrations.

## What We Did

### Migration 1: Extract Metadata Fields (d5b976a1f66e)
Extracted commonly-used fields from `metadata_json` into dedicated columns:

| Column | Source (metadata_json) | Items | Purpose |
|--------|----------------------|-------|---------|
| `lyrics` | Στίχοι | 537 | Game content - songs, lyrics search |
| `recording_date` | Χρονολογία ηχογράφησης | 3,077 | Era classification (1920-1944) |
| `matrix_number` | Αριθμός μήτρας | 3,050 | Catalog reference |
| `dance_rhythm` | Χορός / Ρυθμός | 1,044 | Gameplay (ζεϊμπέκικος, χασάπικο, etc.) |
| `singers` | Τραγουδιστές | 3,089 | Artist information |
| `duration` | Διάρκεια | 3,146 | Track length |
| `recording_place` | Τόπος ηχογράφησης | 3,094 | Geographic data |

**Indexes created:**
- `ix_items_recording_date` - Query by era
- `ix_items_dance_rhythm` - Filter by rhythm type

### Migration 2: Full-Text Search (9edfb5383e88)
Created **FTS5 virtual table** (`items_fts`) for efficient text search across:
- `lyrics` - Primary search field
- `title` - Song titles
- `first_words` - Opening lyrics
- `creator_composer` - Artist names

**Auto-sync triggers** keep FTS table in sync with `items` table.

## Database Structure (Post-Migration)

```
items (main table)
├── Original columns (id, url, title, item_type, etc.)
├── Extracted columns (lyrics, recording_date, matrix_number, etc.)
└── metadata_json (remaining misc. fields)

items_fts (FTS5 virtual table)
└── Full-text search index
```

## Common Alembic Commands

```bash
# Check current migration version
uv run alembic current

# View migration history
uv run alembic history

# Create a new migration
uv run alembic revision -m "description_of_change"

# Apply all pending migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Rollback to specific version
uv run alembic downgrade d5b976a1f66e
```

## Example Queries

### Search lyrics with full-text search
```sql
SELECT i.title, i.creator_composer, i.lyrics
FROM items_fts
JOIN items i ON items_fts.rowid = i.rowid
WHERE items_fts MATCH 'θάλασσα OR μάνα'
LIMIT 10;
```

### Find rebetiko-era songs with lyrics
```sql
SELECT title, creator_composer, recording_date, dance_rhythm
FROM items
WHERE lyrics IS NOT NULL
  AND recording_date LIKE '%192%' OR recording_date LIKE '%193%'
ORDER BY recording_date;
```

### Filter by dance rhythm
```sql
SELECT title, dance_rhythm, duration
FROM items
WHERE dance_rhythm LIKE '%ζεϊμπέκικος%'
  OR dance_rhythm LIKE '%χασάπικος%';
```

## Version Control Strategy

### What's in Git
✅ Migration scripts (`alembic/versions/*.py`)
✅ Configuration (`alembic.ini`, `alembic/env.py`)
✅ This documentation
❌ Database files (`.db` - too large, binary)

### Database Backups
Backups are created automatically before migrations in:
```
database/vmrebetiko_all_genres_archive/backup_before_migration_YYYYMMDD_HHMMSS.db
```

### Reproducibility
Anyone can rebuild the database:
1. Get source database (`vmrebetiko_source.db`)
2. Run `uv run alembic upgrade head`
3. All transformations are applied via versioned scripts

## Creating New Migrations

### When to create a migration:
- Adding/removing/modifying columns
- Creating/dropping indexes
- Changing data types
- Transforming existing data

### Example workflow:
```bash
# 1. Create migration
uv run alembic revision -m "add_song_genre_column"

# 2. Edit the generated file in alembic/versions/
# Implement upgrade() and downgrade() functions

# 3. Test the migration
uv run alembic upgrade head

# 4. Verify changes
uv run python tools/query_db.py  # or use MCP SQLite tools

# 5. Commit migration script to git
git add alembic/versions/*.py
git commit -m "feat: add song genre column for categorization"
```

## Best Practices

1. **Always backup before migrations** - Automatic, but verify
2. **Test migrations both ways** - Run upgrade, then downgrade, then upgrade again
3. **Keep migrations focused** - One logical change per migration
4. **Document the "why"** - Explain purpose in migration docstring
5. **Use batch operations** - For SQLite, always use `op.batch_alter_table()`
6. **Index strategically** - Only index columns used in WHERE/JOIN clauses

## Troubleshooting

### Migration fails mid-way
```bash
# Check current state
uv run alembic current

# If stuck, manually fix and stamp version
uv run alembic stamp head
```

### Need to rollback
```bash
# Rollback last migration
uv run alembic downgrade -1

# Rollback to specific version
uv run alembic downgrade <revision_id>
```

### Lost track of migrations
```bash
# View full history
uv run alembic history --verbose

# Show current + pending
uv run alembic current
uv run alembic heads
```

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLite FTS5 Extension](https://www.sqlite.org/fts5.html)
- Project analysis: `database/analysis/`
- Database schema: Check with MCP SQLite tools
