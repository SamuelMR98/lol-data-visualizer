# analytics/src/ldv_ana/lol/ingest/riot_api.py
from __future__ import annotations
import requests

class RiotAPI:
    def __init__(self, api_key: str, regional_routing: str):
        self.api_key = api_key
        self.base = f"https://{regional_routing}.api.riotgames.com"

    def _get(self, path: str) -> dict:
        url = self.base + path
        r = requests.get(url, headers={"X-Riot-Token": self.api_key}, timeout=30)
        r.raise_for_status()
        return r.json()

    def get_match(self, match_id: str) -> dict:
        return self._get(f"/lol/match/v5/matches/{match_id}")

    def get_timeline(self, match_id: str) -> dict:
        return self._get(f"/lol/match/v5/matches/{match_id}/timeline")