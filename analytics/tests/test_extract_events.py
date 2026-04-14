import polars as pl
from ldv_ana.lol.transform.events import extract_events

def test_extract_events_minimal():
    match_json = {
        "info": {
            "participants": [
                {"participantId": 1, "teamId": 100, "summonerName": "Me", "championName": "Ahri", "teamPosition": "MIDDLE"}
            ]
        }
    }
    timeline_json = {
        "info": {
            "frames": [
                {"events": [
                    {"type":"WARD_PLACED","timestamp":1000,"creatorId":1,"wardType":"YELLOW_TRINKET","position":{"x":5000,"y":5000}},
                    {"type":"CHAMPION_KILL","timestamp":2000,"killerId":1,"victimId":2,"assistingParticipantIds":[],"position":{"x":6000,"y":7000}},
                ]}
            ]
        }
    }

    df = extract_events("TEST_MATCH", match_json, timeline_json)
    assert isinstance(df, pl.DataFrame)
    assert df.height == 2
    assert set(df["event_type"].to_list()) == {"WARD_PLACED", "CHAMPION_KILL"}