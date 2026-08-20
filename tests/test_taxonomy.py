from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
FRAGMENT_PATH = ROOT / "taxonomy.fragment.html"
RENDER_PATH = ROOT / "render.py"
TITLE = "LiDAR Localization Taxonomy"

VALID_TYPES = {"handcrafted", "learned", "geometric", "integrated"}
INTENTIONALLY_UNLINKED = {
    "Nearest neighbour",
    "Mutual check",
    "FPFH + sample consensus + ICP",
}

METHOD_RECORD = re.compile(
    r"^\s*\{\s*year:\s*'(?P<year>[^']+)'\s*,\s*"
    r"name:\s*'(?P<name>[^']+)'\s*,\s*"
    r"note:\s*'(?P<note>[^']+)'\s*,\s*"
    r"type:\s*'(?P<type>[^']+)'(?P<tail>.*?)\}\s*,?\s*$"
)
PAPER_FIELD = re.compile(r",\s*paper:\s*'(?P<paper>[^']+)'\s*$")


def read_fragment() -> str:
    return FRAGMENT_PATH.read_text(encoding="utf-8")


def method_records(fragment: str) -> list[dict[str, str | None]]:
    records: list[dict[str, str | None]] = []
    for line_number, line in enumerate(fragment.splitlines(), start=1):
        if not line.lstrip().startswith("{ year:"):
            continue
        match = METHOD_RECORD.match(line)
        if match is None:
            raise AssertionError(f"Malformed method record on line {line_number}: {line}")
        record: dict[str, str | None] = match.groupdict()
        paper_match = PAPER_FIELD.fullmatch(record.pop("tail") or "")
        record["paper"] = paper_match.group("paper") if paper_match else None
        records.append(record)
    return records


class TaxonomyTests(unittest.TestCase):
    def test_renderer_produces_a_standalone_document(self) -> None:
        from render import render

        fragment = read_fragment()
        rendered = render(fragment, TITLE)

        self.assertTrue(rendered.startswith("<!doctype html>"))
        self.assertIn(f"<title>{TITLE}</title>", rendered)
        self.assertIn(fragment.rstrip(), rendered)
        self.assertNotIn("<iframe", rendered.lower())
        self.assertEqual(rendered.count('id="pcr-literature-taxonomy"'), 1)

    def test_renderer_cli_matches_the_render_function(self) -> None:
        from render import render

        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "taxonomy.html"
            subprocess.run(
                [sys.executable, str(RENDER_PATH), str(FRAGMENT_PATH), str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                render(read_fragment(), TITLE),
            )

    def test_method_records_and_paper_links_are_valid(self) -> None:
        records = method_records(read_fragment())

        self.assertGreater(len(records), 50)
        self.assertEqual(
            {record["name"] for record in records if record["paper"] is None},
            INTENTIONALLY_UNLINKED,
        )

        for record in records:
            with self.subTest(method=record["name"]):
                self.assertTrue(record["year"])
                self.assertTrue(record["name"])
                self.assertTrue(record["note"])
                self.assertIn(record["type"], VALID_TYPES)

                paper = record["paper"]
                if paper is None:
                    continue
                parsed = urlparse(paper)
                self.assertEqual(parsed.scheme, "https")
                self.assertTrue(parsed.netloc)
                if parsed.netloc == "arxiv.org":
                    self.assertTrue(parsed.path.startswith("/abs/"))

    def test_category_buttons_match_taxonomy_categories(self) -> None:
        fragment = read_fragment()
        button_categories = set(re.findall(r'data-category="([a-z]+)"', fragment))
        data_categories = set(
            re.findall(r"^        ([a-z]+): \{$", fragment, flags=re.MULTILINE)
        )

        self.assertIn("retrieval", data_categories)
        self.assertEqual(button_categories, data_categories)

    def test_external_links_use_safe_new_tab_attributes(self) -> None:
        fragment = read_fragment()

        self.assertIn("name.target = '_blank';", fragment)
        self.assertIn("name.rel = 'noopener noreferrer';", fragment)


if __name__ == "__main__":
    unittest.main()
