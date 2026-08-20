#!/usr/bin/env python3
"""Render the editable taxonomy fragment as one self-contained HTML file."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path


BASE_CSS = """
:root {
  color-scheme: light dark;
  --background: light-dark(rgb(255 255 255), rgb(24 24 24));
  --foreground: light-dark(rgb(26 28 31), rgb(245 245 245));
  --muted-foreground: light-dark(rgb(90 94 100), rgb(178 181 186));
  --primary: light-dark(rgb(24 112 201), rgb(131 195 255));
  --primary-foreground: light-dark(rgb(255 255 255), rgb(13 13 13));
  --secondary: light-dark(rgb(244 245 247), rgb(48 48 48));
  --secondary-foreground: var(--foreground);
  --border: light-dark(rgb(26 28 31 / 16%), rgb(255 255 255 / 18%));
  --ring: var(--primary);
  --viz-series-1: light-dark(rgb(24 112 201), rgb(131 195 255));
  --viz-series-2: light-dark(rgb(0 132 84), rgb(78 205 148));
  --viz-series-3: light-dark(rgb(126 74 175), rgb(195 145 239));
  --viz-series-4: light-dark(rgb(196 92 20), rgb(255 158 91));
  --font-size-base: 15px;
  background: var(--background);
  color: var(--foreground);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  font-size: var(--font-size-base);
}

* { box-sizing: border-box; }

body {
  margin: 0 auto;
  max-width: 1180px;
  min-width: 320px;
  padding: clamp(1rem, 3vw, 2.5rem);
}

button, a { font: inherit; }
a { color: var(--primary); }

h3 {
  font-size: clamp(1.25rem, 3vw, 1.75rem);
  font-weight: 500;
  margin: 0;
}

.text-small { font-size: 0.86rem; }
.viz-controls { align-items: center; display: flex; flex-wrap: wrap; }

.btn {
  appearance: none;
  background: var(--secondary);
  border: 1px solid var(--border);
  border-radius: 0.45rem;
  color: var(--secondary-foreground);
  cursor: pointer;
  padding: 0.5rem 0.75rem;
}

.btn:hover { border-color: var(--primary); }
.btn:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
.btn-primary { background: var(--primary); color: var(--primary-foreground); }
""".strip()


def render(fragment: str, title: str) -> str:
    """Wrap a visualization fragment in a portable standalone document."""
    safe_title = escape(title)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="referrer" content="no-referrer">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; object-src 'none'; base-uri 'none'; form-action 'none'">
  <title>{safe_title}</title>
  <style>
{BASE_CSS}
  </style>
</head>
<body>
{fragment.rstrip()}
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("taxonomy.fragment.html"),
        help="Editable HTML fragment",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("index.html"),
        help="Generated standalone HTML",
    )
    parser.add_argument(
        "--title",
        default="LiDAR Localization Taxonomy",
    )
    args = parser.parse_args()

    fragment = args.source.read_text(encoding="utf-8")
    args.output.write_text(render(fragment, args.title), encoding="utf-8")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
