from __future__ import annotations
from typing import Any
import polars as pl

# Approx SR bounds (good enough for MVP overlays; refine later if needed)
SR_MIN_X, SR_MAX_X = -120, 14870
SR_MIN_Y, SR_MAX_Y = -120, 14980

def _pos(evt: dict) -> tuple[int | None, int | None]:
    p = evt.get("position")
    if not isinstance(p, dict):
        return None, None
    return p.get("x"), p.get("y")

def extract_events(match_id: str, match_json: dict, timeline_json: dict) -> pl.DataFrame:
    """
    Extract minimal event telemetry from Match-V5 timeline:
      - WARD_PLACED
      - CHAMPION_KILL
    Output schema is stable for appending to Parquet.
    """
    info = match_json.get("info", {})
    participants = info.get("participants", [])

    # participantId (1..10) -> metadata (team, champ, role, summoner)
    pid_map: dict[int, dict[str, Any]] = {}
    for p in participants:
        pid = p.get("participantId")
        if isinstance(pid, int):
            pid_map[pid] = {
                "team_id": p.get("teamId"),
                "summoner_name": p.get("summonerName"),
                "champion": p.get("championName"),
                "team_position": p.get("teamPosition"),
            }

    rows: list[dict[str, Any]] = []
    frames = timeline_json.get("info", {}).get("frames", [])
    for fr in frames:
        for evt in fr.get("events", []):
            et = evt.get("type")
            ts = evt.get("timestamp")
            x, y = _pos(evt)

            if et == "WARD_PLACED":
                creator = evt.get("creatorId")
                meta = pid_map.get(creator, {})
                rows.append({
                    "match_id": match_id,
                    "ts_ms": ts,
                    "event_type": et,
                    "actor_id": creator,
                    "target_id": None,
                    "x": x, "y": y,
                    "ward_type": evt.get("wardType"),
                    "assists": None,
                    **meta,
                })

            elif et == "CHAMPION_KILL":
                killer = evt.get("killerId")
                victim = evt.get("victimId")
                meta = pid_map.get(killer, {})
                rows.append({
                    "match_id": match_id,
                    "ts_ms": ts,
                    "event_type": et,
                    "actor_id": killer,
                    "target_id": victim,
                    "x": x, "y": y,
                    "ward_type": None,
                    "assists": evt.get("assistingParticipantIds", []),
                    **meta,
                })

    if rows:
        return pl.DataFrame(rows)

    # empty DF with stable schema
    return pl.DataFrame(
        schema={
            "match_id": pl.Utf8,
            "ts_ms": pl.Int64,
            "event_type": pl.Utf8,
            "actor_id": pl.Int64,
            "target_id": pl.Int64,
            "x": pl.Int64,
            "y": pl.Int64,
            "ward_type": pl.Utf8,
            "assists": pl.List(pl.Int64),
            "team_id": pl.Int64,
            "summoner_name": pl.Utf8,
            "champion": pl.Utf8,
            "team_position": pl.Utf8,
        }
    )