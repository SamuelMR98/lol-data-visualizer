from __future__ import annotations
from pathlib import Path
import json
import polars as pl

def append_parquet(df: pl.DataFrame, path: Path, unique_cols: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        df.write_parquet(str(path))
        return

    existing = pl.read_parquet(str(path))
    combined = pl.concat([existing, df], how="diagonal")

    if unique_cols:
        combined = combined.unique(subset=unique_cols, keep="last")

    combined.write_parquet(str(path))

def write_by_match_json(match_id: str, df: pl.DataFrame, out_dir: Path, bounds: dict) -> Path:
    """
    Writes a JSON file that Go can serve easily later.
    Structure:
      { match_id, bounds, events: [ {ts_ms,event_type,x,y,...}, ... ] }
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{match_id}.json"

    payload = {
        "match_id": match_id,
        "bounds": bounds,
        "events": df.to_dicts(),
    }
    out_path.write_text(json.dumps(payload, indent=2))
    return out_path