from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2))

def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())