import argparse
import polars as pl
from ldv.config import get_config
from ldv.core.viz.heatmap import plot_heatmap


def main(match_id: str, typ: str) -> None:
    cfg = get_config()
    events_path = f"{cfg.data_processed_dir}/events.parquet"
    df = pl.read_parquet(events_path).filter(pl.col("match_id") == match_id)

    if typ == "wards":
        df = df.filter(pl.col("event_type") == "WARD_PLACED")
        title = f"Ward placements — {match_id}"
        out = f"{cfg.data_processed_dir}/heatmap_wards_{match_id}.png"
    elif typ == "kills":
        df = df.filter(pl.col("event_type") == "CHAMPION_KILL")
        title = f"Kill locations — {match_id}"
        out = f"{cfg.data_processed_dir}/heatmap_kills_{match_id}.png"
    else:
        raise ValueError("type must be 'wards' or 'kills'")

    plot_heatmap(df, cfg.minimap_path, title, out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--match", required=True)
    p.add_argument("--type", required=True, choices=["wards", "kills"])
    args = p.parse_args()
    main(args.match, args.type)