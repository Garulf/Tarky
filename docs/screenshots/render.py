"""Render the README screenshots and hero image with flow-render.

Usage (from the repo root, with flow-render 0.15.0 installed):

    pip install flow-render==0.15.0
    python docs/screenshots/render.py

or ``tox -e screenshots``.

Each ``<shot>.json`` is a flow-render config whose results name a tarkov.dev
item ID in ``item`` instead of an ``icon``. The item icons are downloaded from
the tarkov.dev image CDN at render time rather than kept in the repo.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHOTS_DIR = ROOT / "docs" / "screenshots"
ASSETS_DIR = ROOT / ".github" / "assets"
THEMES = ["dark", "light"]
HERO = {"shot": "hero", "theme": "dark", "css": ["win11-dark.css", "docs/screenshots/hero.css"]}
ICON_URL = "https://assets.tarkov.dev/{item}-icon.webp"


def item_icon(item: str, out_dir: Path) -> Path:
    path = out_dir / f"{item}.webp"
    if not path.exists():
        request = urllib.request.Request(ICON_URL.format(item=item), headers={"User-Agent": "Tarky-screenshots"})
        with urllib.request.urlopen(request, timeout=30) as response:
            path.write_bytes(response.read())
    return path


def flow_render(args, out_path: Path) -> None:
    with tempfile.TemporaryDirectory() as out_dir:
        subprocess.run(["flow-render", *args, "-o", out_dir], check=True, cwd=ROOT)
        (rendered,) = Path(out_dir).glob("*.png")
        shutil.move(str(rendered), out_path)
    print(f"Wrote {out_path}")


def render_config(shot: str, css, out_path: Path, work: Path) -> None:
    config = json.loads((SHOTS_DIR / f"{shot}.json").read_text(encoding="utf-8"))
    config["icon"] = str((SHOTS_DIR / config["icon"]).resolve())
    for result in config["results"]:
        result["icon"] = str(item_icon(result.pop("item"), work))
    config["css"] = css
    config_path = work / f"{shot}.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    flow_render(["-c", str(config_path)], out_path)


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    shots = sorted(path.stem for path in SHOTS_DIR.glob("*.json") if path.stem != HERO["shot"])
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for shot in shots:
            for theme in THEMES:
                render_config(shot, f"win11-{theme}.css", ASSETS_DIR / f"{shot}-{theme}.png", work)
        render_config(HERO["shot"], HERO["css"], ASSETS_DIR / "hero.png", work)


if __name__ == "__main__":
    sys.exit(main())
