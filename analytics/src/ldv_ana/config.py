from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

def _load_env_from_repo_root() -> None:
    # repo_root = analytics/.. (parent of this file's parents)
    repo_root = Path(__file__).resolve().parents[3]
    load_dotenv(repo_root / ".env")

@dataclass(frozen=True)
class Config:
    riot_api_key: str
    regional_routing: str

    repo_root: Path
    data_raw_matches: Path
    data_raw_timelines: Path
    data_processed_dir: Path
    events_parquet: Path
    by_match_dir: Path
    minimap_path: Path

def get_config() -> Config:
    _load_env_from_repo_root()
    key = os.getenv("RIOT_API_KEY", "").strip()
    routing = os.getenv("RIOT_REGIONAL_ROUTING", "americas").strip()
    if not key:
        raise RuntimeError("Missing RIOT_API_KEY (set it in repo root .env)")

    repo_root = Path(__file__).resolve().parents[3]
    data_root = repo_root / "data"
    assets_root = repo_root / "assets"

    return Config(
        riot_api_key=key,
        regional_routing=routing,
        repo_root=repo_root,
        data_raw_matches=data_root / "raw" / "lol" / "matches",
        data_raw_timelines=data_root / "raw" / "lol" / "timelines",
        data_processed_dir=data_root / "processed" / "lol",
        events_parquet=data_root / "processed" / "lol" / "events.parquet",
        by_match_dir=data_root / "processed" / "lol" / "by_match",
        minimap_path=assets_root / "lol" / "maps" / "summoners_rift_minimap.png",
    )
