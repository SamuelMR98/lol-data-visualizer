from __future__ import annotations
from ldv_ana.lol.transform.events import SR_MIN_X, SR_MAX_X, SR_MIN_Y, SR_MAX_Y

def to_image_xy(x: int, y: int, img_w: int, img_h: int) -> tuple[float, float]:
    nx = (x - SR_MIN_X) / (SR_MAX_X - SR_MIN_X)
    ny = (y - SR_MIN_Y) / (SR_MAX_Y - SR_MIN_Y)
    px = nx * img_w
    py = (1.0 - ny) * img_h
    return px, py