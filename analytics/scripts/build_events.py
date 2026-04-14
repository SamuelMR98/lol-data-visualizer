#!/usr/bin/env python3
import sys
from ldv_ana.config import get_config
from ldv_ana.lol.ingest.cache import read_json
from ldv_ana.lol.transform.events import extract_events, SR_MIN_X, SR_MAX_X, SR_MIN_Y, SR_MAX_Y
from ldv_ana.core.storage import append_parquet, write_by_match_json

def main(match_id: str) -> None:
    cfg = get_config()
    match_path = cfg.data_raw_matches / f"{match_id}.json"
    timeline_path = cfg.data_raw_timelines / f"{match_id}.json"

    match_json = read_json(match_path)
    timeline_json = read_json(timeline_path)
    if match_json is None or timeline_json is None:
        raise RuntimeError("Missing raw JSON. Run ingest_match.py first.")

    df = extract_events(match_id, match_json, timeline_json)

    append_parquet(
        df,
        cfg.events_parquet,
        unique_cols=["match_id", "ts_ms", "event_type", "actor_id", "target_id", "x", "y"],
    )

    bounds = {"minX": SR_MIN_X, "maxX": SR_MAX_X, "minY": SR_MIN_Y, "maxY": SR_MAX_Y}
    out_json = write_by_match_json(match_id, df, cfg.by_match_dir, bounds)

    print(f"Events rows: {df.height}")
    print(f"Appended -> {cfg.events_parquet}")
    print(f"Wrote -> {out_json}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/build_events.py <match_id>")
    main(sys.argv[1])