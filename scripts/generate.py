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
        "## Experience",
        "",
    ]

    for job in cfg["experience"]:
        dates = f"{job['start']} – {job['end']}"
        lines.append(f"### {job['role']} @ {job['org']}")
        lines.append(f"*{job['location']} · {dates}*")
        lines.append("")
        for bullet in job["bullets"]:
            lines.append(f"- {bullet}")
        lines.append("")

    lines.append("## Education")
    lines.append("")
    for edu in cfg["education"]:
        dates = ""
        if edu.get("start") or edu.get("end"):
            dates = f" ({edu.get('start', '')} – {edu.get('end', '')})".strip()
        lines.append(f"- **{edu['school']}** — {edu['degree']}{dates}")
    lines.append("")

    skills = cfg["skills"]
    lines.append("## Skills")
    lines.append("")
    lines.append(f"- **Programming:** {', '.join(skills['programming'])}")
    lines.append(
        f"- **Infrastructure:** {', '.join(skills['infrastructure'])}")
    lines.append(
        f"- **Machine Learning:** {', '.join(skills['machine_learning'])}")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    cfg = load_config()
    OUT_PROFILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROFILE.write_text(render_readme(cfg))
    print(f"Wrote {OUT_PROFILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
