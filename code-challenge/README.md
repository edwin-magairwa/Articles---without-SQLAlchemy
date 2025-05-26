# Object Relations Code Challenge: Authors, Articles, and Magazines

This project models relationships between Authors, Articles, and Magazines using Python and SQLite, following OOP principles and raw SQL queries (no ORM).

## Project Structure

- `lib/` - Core library code
  - `models/` - Model classes for Author, Article, Magazine
  - `db/` - Database connection, schema, and seed scripts
  - `controllers/` - (Reserved for future use)
- `tests/` - Pytest-based unit tests
- `scripts/` - Setup and CLI scripts

## Setup Instructions

1. **Create a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install pytest
   ```
3. **Initialize the database:**
   ```bash
   python scripts/setup_db.py
   ```

## Running Tests

```bash
pytest
```

## Using the CLI

```bash
python scripts/run_queries.py
```

## Features
- Raw SQL queries (no ORM)
- OOP model classes
- Transaction handling and SQL injection protection
- Comprehensive test coverage
- Interactive CLI for querying data
