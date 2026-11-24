#!/usr/bin/env python3
"""Generate profile README.md and portfolio index.html from config.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"
OUT_PROFILE = ROOT / "dist" / "profile" / "README.md"
OUT_PORTFOLIO = ROOT / "dist" / "portfolio" / "index.html"


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
    lines.append(f"- **Infrastructure:** {', '.join(skills['infrastructure'])}")
    lines.append(f"- **Machine Learning:** {', '.join(skills['machine_learning'])}")
    lines.append("")

    return "\n".join(lines)


def render_index(cfg: dict) -> str:
    p = cfg["profile"]

    experience_html = []
    for job in cfg["experience"]:
        bullets = "\n".join(f"        <li>{b}</li>" for b in job["bullets"])
        experience_html.append(
            f"""    <section>
      <h3>{job['role']} @ {job['org']}</h3>
      <p class="meta">{job['location']} · {job['start']} – {job['end']}</p>
      <ul>
{bullets}
      </ul>
    </section>"""
        )

    education_html = []
    for edu in cfg["education"]:
        dates = ""
        if edu.get("start") or edu.get("end"):
            dates = f" · {edu.get('start', '')} – {edu.get('end', '')}"
        education_html.append(
            f"      <li><strong>{edu['school']}</strong> — {edu['degree']}{dates}</li>"
        )

    skills = cfg["skills"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{p['name']} — {p['title']}</title>
  <style>
    :root {{
      --bg: #f7f5f1;
      --ink: #1a1a1a;
      --muted: #555;
      --accent: #0b3d2e;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
      background: linear-gradient(160deg, #f7f5f1 0%, #e8efe9 100%);
      color: var(--ink);
      line-height: 1.55;
    }}
    main {{
      max-width: 720px;
      margin: 0 auto;
      padding: 3rem 1.25rem 4rem;
    }}
    h1 {{
      margin: 0 0 0.25rem;
      font-size: 2.25rem;
      letter-spacing: -0.02em;
      color: var(--accent);
    }}
    .title {{ margin: 0; font-size: 1.1rem; color: var(--muted); }}
    .tagline {{ margin: 1rem 0 1.5rem; }}
    a {{ color: var(--accent); }}
    h2 {{
      margin: 2.5rem 0 1rem;
      font-size: 1.15rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--accent);
      border-bottom: 1px solid #c9d4cc;
      padding-bottom: 0.35rem;
    }}
    h3 {{ margin: 0 0 0.25rem; font-size: 1.05rem; }}
    .meta {{ margin: 0 0 0.5rem; color: var(--muted); font-size: 0.9rem; }}
    section {{ margin-bottom: 1.5rem; }}
    ul {{ padding-left: 1.2rem; }}
    li {{ margin-bottom: 0.35rem; }}
  </style>
</head>
<body>
  <main>
    <h1>{p['name']}</h1>
    <p class="title">{p['title']} · {p['location']}</p>
    <p class="tagline">{p['tagline']}</p>
    <p>
      <a href="{p['links']['github']}">GitHub</a>
      ·
      <a href="{p['links']['portfolio']}">{p['links']['portfolio'].replace('https://', '')}</a>
    </p>

    <h2>Experience</h2>
{chr(10).join(experience_html)}

    <h2>Education</h2>
    <ul>
{chr(10).join(education_html)}
    </ul>

    <h2>Skills</h2>
    <ul>
      <li><strong>Programming:</strong> {', '.join(skills['programming'])}</li>
      <li><strong>Infrastructure:</strong> {', '.join(skills['infrastructure'])}</li>
      <li><strong>Machine Learning:</strong> {', '.join(skills['machine_learning'])}</li>
    </ul>
  </main>
</body>
</html>
"""


def main() -> None:
    cfg = load_config()
    OUT_PROFILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_PORTFOLIO.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROFILE.write_text(render_readme(cfg))
    OUT_PORTFOLIO.write_text(render_index(cfg))
    print(f"Wrote {OUT_PROFILE.relative_to(ROOT)}")
    print(f"Wrote {OUT_PORTFOLIO.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
