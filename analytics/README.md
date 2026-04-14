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

Match id = LA1_{match_id} (e.g. LA1_1234567890)
This works for LAN, but for other regions the prefix may differ (e.g. NA1, EUW1, etc.). The prefix indicates the platform/region of the match. You can find the correct prefix for your region in the Riot API documentation or by checking existing match IDs from that region.