from __future__ import annotations
from pathlib import Path
import polars as pl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from ldv_ana.lol.viz.map_coords import to_image_xy

def plot_heatmap(df: pl.DataFrame, minimap_path: Path, title: str, out_path: Path) -> None:
    img = mpimg.imread(str(minimap_path))
    h, w = img.shape[0], img.shape[1]

    pts = df.drop_nulls(["x", "y"]).select(["x", "y"]).to_numpy()
    xs, ys = [], []
    for x, y in pts:
        px, py = to_image_xy(int(x), int(y), w, h)
        xs.append(px)
        ys.append(py)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    if xs:
        plt.hexbin(xs, ys, gridsize=60, mincnt=1, alpha=0.55)
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(str(out_path), dpi=200)
    plt.close()