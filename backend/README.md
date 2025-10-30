# TruCon NDTS Backend

This is the national-grade, trust-first data API for Nigerian Data Trust System (TruCon).

## Quickstart

1. Install Python 3.9+/pip
2. Create & activate virtualenv
3. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
4. Start the dev server:
   ```sh
   uvicorn backend.main:app --reload
   ```
5. Open http://localhost:8000/health

## Directory Structure
- `main.py`        – FastAPI app bootstrap
- `requirements.txt` – Core dependencies
- `models/`        – Data models (soon)
- `services/`      – Service logic (soon)
- `alembic/`       – Database migrations (optional, via Alembic)

For full design spec, see `../backend.md`.

## Next Steps
- Scaffold full DB models, services per backend.md
- Connect real database (PostgreSQL)
- Implement JWT auth, role system
- Add OpenAPI docs and endpoints
