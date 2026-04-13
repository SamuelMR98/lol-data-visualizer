# ldv-analytics (Python)

## MVP Plan

MVP:

1) Ingest match+timeline JSON (cached under ../data/raw/lol)
2) Extract events (WARD_PLACED + CHAMPION_KILL with x,y)
3) Append to ../data/processed/lol/events.parquet
4) Write per-match JSON to ../data/processed/lol/by_match/<match_id>.json
5) Generate a minimap heatmap PNG

## Setup

From repo root:

```bash
cd analytics
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```