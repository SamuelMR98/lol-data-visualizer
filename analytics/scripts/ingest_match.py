import sys
from ldv.config import get_config
from ldv.lol.ingest.riot_api import RiotAPI
from ldv.lol.ingest.cache import ensure_dir, write_json, read_json


def main(match_id: str) -> None:
    cfg = get_config()
    api = RiotAPI(cfg.riot_api_key, cfg.regional_routing)

    ensure_dir(cfg.data_raw_matches)
    ensure_dir(cfg.data_raw_timelines)

    match_path = f"{cfg.data_raw_matches}/{match_id}.json"
    timeline_path = f"{cfg.data_raw_timelines}/{match_id}.json"

    if read_json(match_path) is None:
        write_json(match_path, api.get_match(match_id))
        print(f"Saved match -> {match_path}")
    else:
        print(f"Match cached -> {match_path}")

    if read_json(timeline_path) is None:
        write_json(timeline_path, api.get_timeline(match_id))
        print(f"Saved timeline -> {timeline_path}")
    else:
        print(f"Timeline cached -> {timeline_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/lol/ingest_match.py <match_id>")
    main(sys.argv[1])