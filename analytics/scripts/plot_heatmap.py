#!/usr/bin/env python3
import argparse
import polars as pl
from ldv_ana.config import get_config
from ldv_ana.lol.viz.heatmap import plot_heatmap

def main(match_id: str, typ: str) -> None:
    cfg = get_config()

    df = pl.read_parquet(str(cfg.events_parquet)).filter(pl.col("match_id") == match_id)

    if typ == "wards":
        df = df.filter(pl.col("event_type") == "WARD_PLACED")
        title = f"Ward placements — {match_id}"
        out = cfg.data_processed_dir / f"heatmap_wards_{match_id}.png"
    else:
        df = df.filter(pl.col("event_type") == "CHAMPION_KILL")
        title = f"Kill locations — {match_id}"
        out = cfg.data_processed_dir / f"heatmap_kills_{match_id}.png"

    plot_heatmap(df, cfg.minimap_path, title, out)
    print(f"Wrote {out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--match", required=True)
    p.add_argument("--type", required=True, choices=["wards", "kills"])
    args = p.parse_args()
    main(args.match, args.type)