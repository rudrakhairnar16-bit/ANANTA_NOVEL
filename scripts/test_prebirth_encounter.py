#!/usr/bin/env python3
"""Protect the user-approved six-years-before-birth Ram–Adhira chronology.

This correction changes timing/child-presence wording, not reveal minima,
training age, the outcome of the old fight or the already-delivered source reward.
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPAIRED_COUNTS = {
    84: 4366, 85: 4356, 86: 4393, 87: 4321, 89: 4353, 92: 4371,
    118: 4374, 119: 4519, 120: 4495, 121: 4603, 123: 4507,
}


class PrebirthEncounterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bible = (ROOT / "ANANTA_MASTER_BIBLE.md").read_text(encoding="utf-8")
        cls.chapters = {
            int(p.name.split("-")[1]): p.read_text(encoding="utf-8")
            for p in ROOT.glob("book-*/ch-*.md")
        }

    def test_relative_interval_controls_approximate_calendar_year(self):
        timeline = self.bible.split("| Year |", 1)[1].split("## PART 7:", 1)[0]
        event = "| ~2001 (six years before Rudra's birth) |"
        birth = "| ~2007 | Rudra born."
        self.assertIn(event, timeline)
        self.assertIn(birth, timeline)
        self.assertLess(timeline.index(event), timeline.index(birth))
        self.assertIn("| 2026 (Story Start) |", timeline)
        authority = self.bible.split("## PART 38:", 1)[1].split("## PART 39:", 1)[0]
        self.assertIn("relative interval controls", authority)
        self.assertIn("not an exact newly established birthday", authority)
        self.assertIn("Kaal FIRST SPOKEN119–120", authority)
        self.assertIn("Training still begins at age one, AFTER the encounter", authority)

    def test_repaired_sources_have_exact_current_counts_and_one_end(self):
        for chapter, words in REPAIRED_COUNTS.items():
            text = self.chapters[chapter]
            with self.subTest(chapter=chapter):
                self.assertNotIn("2020", text)
                self.assertEqual(text.count("### END OF CHAPTER"), 1)
                self.assertTrue(text.endswith(f"### END OF CHAPTER {chapter}\n"))
                self.assertEqual(len(text.split("### END OF CHAPTER", 1)[0].split()), words)
                self.assertTrue(4300 <= words <= 6200)

    def test_impossible_child_presence_and_reversed_training_order_are_absent(self):
        old = (
            "That year belonged to his own memory.",
            "while Rudra was still going to classes",
            "He had come home, and a boy had been there",
            "training had already been going on for years before that encounter",
            "begun the boy's training long before 2020",
            "boy who might remember 2020",
        )
        joined = "\n".join(self.chapters[n] for n in REPAIRED_COUNTS)
        for impossible in old:
            with self.subTest(impossible=impossible):
                self.assertNotIn(impossible, joined)
        self.assertIn("no child waiting for him then", self.chapters[84])
        self.assertIn("had not witnessed that return", self.chapters[85])
        self.assertIn("training had come years later", self.chapters[86])
        self.assertIn("training, which began when he was one", self.chapters[87])
        self.assertIn("By the time training began at one, Ram had long carried it", self.chapters[119])

    def test_training_age_and_family_accountability_are_not_rewritten(self):
        self.assertIn("**Training Rudra:** Started at age 1.", self.bible)
        self.assertIn('"Main ek saal ka tha, Papa,"', self.chapters[85])
        self.assertIn('"Ek saal ki umar se?"', self.chapters[86])
        self.assertIn('"Mere hukm mere the," Ram said.', self.chapters[119])
        self.assertIn("could not supply a child's consent", self.chapters[85])

    def test_repaired_hooks_and_original_reveal_placement_stay_connected(self):
        self.assertIn('"Mere janam se chhe saal pehle kya hua tha, Papa?"', self.chapters[84])
        self.assertIn('"Adhira se lada tha," Ram said. "Tumhaare janam se chhe saal pehle.', self.chapters[85])
        self.assertIn('"Papa, mere janam se chhe saal pehle aapko kis tarah pata chala tha', self.chapters[123])
        for n in range(81, 119):
            with self.subTest(chapter=n):
                self.assertNotRegex(self.chapters[n], re.compile(r"\bKaal\b", re.I))
        self.assertIn('\n"Kaal," Ram said.\n', self.chapters[119])
        self.assertIn('"Aur woh theek nahi chal rahi,"', self.chapters[119])
        self.assertIn('"Mujhe nahi pata, beta.', self.chapters[120])

    def test_book7_merge_still_uses_each_numeric_source_once(self):
        directory = ROOT / "book-07"
        sources = sorted(directory.glob("ch-*.md"), key=lambda p: int(p.name.split("-")[1]))
        numbers = [int(p.name.split("-")[1]) for p in sources]
        self.assertEqual(numbers, list(range(121, max(numbers) + 1)))
        expected = "# ANANTA — BOOK 07 — MERGED\n\n"
        expected += "\n\n".join(p.read_text(encoding="utf-8").split("### END OF CHAPTER", 1)[0].strip() for p in sources) + "\n"
        self.assertEqual((directory / "ANANTA-BOOK-07-MERGED.md").read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
