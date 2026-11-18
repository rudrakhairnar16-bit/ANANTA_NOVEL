#!/usr/bin/env python3
"""Regressions for the user-approved Book4–6 title metadata.

Titles affect only each merged book's first line. Current exact source counts
include the separately user-approved pre-birth chronology repair (Bible Part38).
Run: python3 -B -m unittest discover -s scripts -p 'test_*.py'
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
APPROVED = (
    (4, "Bloodlines at War", 61, 80, 89189),
    (5, "The Asuran Legacy", 81, 100, 87082),
    (6, "Unbound: Pataal", 101, 120, 87725),
)


class ApprovedBookTitleTests(unittest.TestCase):
    def test_bible_records_exact_approved_titles_and_stable_paths(self):
        bible = (ROOT / "ANANTA_MASTER_BIBLE.md").read_text(encoding="utf-8")
        approval = bible.split("## PART 36:", 1)[1].split("## PART 37:", 1)[0]
        for number, title, start, end, _ in APPROVED:
            path = f"book-{number:02d}/ANANTA-BOOK-{number:02d}-MERGED.md"
            with self.subTest(book=number):
                self.assertIn(f"| {number} | {title} | {start}–{end} | `{path}` |", approval)
        self.assertIn("every byte AFTER the first line unchanged", approval)
        self.assertIn("not permission to edit the chapter bodies", approval)

    def test_readme_links_display_the_approved_titles(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for number, title, start, end, _ in APPROVED:
            path = f"book-{number:02d}/ANANTA-BOOK-{number:02d}-MERGED.md"
            with self.subTest(book=number):
                self.assertIn(f"| {number} | [{title}]({path}) | {start}–{end} |", readme)
                self.assertTrue((ROOT / path).is_file())

    def test_titled_merges_match_the_exact_numeric_end_stripped_sources(self):
        for number, title, start, end, _ in APPROVED:
            directory = ROOT / f"book-{number:02d}"
            sources = sorted(directory.glob("ch-*.md"), key=lambda p: int(p.name.split("-")[1]))
            with self.subTest(book=number):
                self.assertEqual([int(p.name.split("-")[1]) for p in sources], list(range(start, end + 1)))
                pieces = []
                for source in sources:
                    chapter = int(source.name.split("-")[1])
                    raw = source.read_text(encoding="utf-8")
                    self.assertEqual(raw.count("### END OF CHAPTER"), 1, source.name)
                    self.assertTrue(raw.endswith(f"### END OF CHAPTER {chapter}\n"), source.name)
                    pieces.append(raw.split("### END OF CHAPTER", 1)[0].strip())
                expected = f"# ANANTA — BOOK {number:02d}: {title.upper()} — MERGED\n\n"
                expected += "\n\n".join(pieces) + "\n"
                merged = directory / f"ANANTA-BOOK-{number:02d}-MERGED.md"
                self.assertEqual(merged.read_text(encoding="utf-8"), expected)

    def test_book_title_words_do_not_change_completed_chapter_totals(self):
        for number, _, _, _, words in APPROVED:
            sources = (ROOT / f"book-{number:02d}").glob("ch-*.md")
            actual = sum(len(p.read_text(encoding="utf-8").split("### END OF CHAPTER", 1)[0].split()) for p in sources)
            with self.subTest(book=number):
                self.assertEqual(actual, words)


if __name__ == "__main__":
    unittest.main()
