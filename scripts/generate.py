#!/usr/bin/env python3
"""Generate profile README.md from config.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"
OUT_PROFILE = ROOT / "dist" / "profile" / "README.md"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def render_readme(cfg: dict) -> str:
    p = cfg["profile"]
    lines = [
        f"# Hi, I'm {p['name']}",
        "",
        f"**{p['title']}** — {p['tagline']}",
        "",
        f"Based in **{p['location']}**.",
        "",
        f"- [GitHub]({p['links']['github']})",
        f"- [Portfolio]({p['links']['portfolio']})",
        f"- [LinkedIn]({p['links']['linkedin']})"
        "",
        "---",
        "",
        "## What I'm Up To",
        "",
        f"I'm currently focused on the **{cfg['spotlight']['name']}**. This is a {cfg['spotlight']['description']}.",
        "",
        "---",
        "",
        "## What I've Done",
        "",
        # only show the first/top 2 projects, will bump to 3 when I get a third project
        for project in cfg['projects'][:2]:
        lines.append(f"- {project['name']}")
        lines.append(f"  - {project['description']}")
        lines.append("")
    ]
    return "\n".join(lines)


def main() -> None:
    cfg = load_config()
    OUT_PROFILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROFILE.write_text(render_readme(cfg))
    print(f"Wrote {OUT_PROFILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
