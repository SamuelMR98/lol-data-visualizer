import sys
from ldv.config import get_config
from ldv.lol.ingest.cache import read_json
from ldv.lol.transform.timeline_events import extract_events
from ldv.core.storage.parquet import append_parquet


def main(match_id: str) -> None:
    cfg = get_config()
    match_path = f"{cfg.data_raw_matches}/{match_id}.json"
    timeline_path = f"{cfg.data_raw_timelines}/{match_id}.json"

    match_json = read_json(match_path)
    timeline_json = read_json(timeline_path)
    if match_json is None or timeline_json is None:
        raise RuntimeError("Missing raw JSON. Run ingest_match.py first.")

    events = extract_events(match_id, match_json, timeline_json)

    out_path = f"{cfg.data_processed_dir}/events.parquet"
    append_parquet(
        events,
        out_path,
        unique_cols=["match_id", "ts_ms", "event_type", "actor_id", "target_id", "x", "y"],
    )
    print(f"Appended {events.height} rows -> {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/lol/build_events.py <match_id>")
    main(sys.argv[1])