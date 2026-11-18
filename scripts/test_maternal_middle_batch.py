#!/usr/bin/env python3
"""Bound133–135: private maternal testimony, not later powers or fresh politics."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MaternalMiddleBatchTests(unittest.TestCase):
    def test133_135_authority_keeps_source_scope_privacy_and_later_gates(self):
        bible = (ROOT / "ANANTA_MASTER_BIBLE.md").read_text(encoding="utf-8")
        batch = bible.split("## PART 42:", 1)[1].split("## PART 43:", 1)[0]
        for phrase in (
            "Ch 133–135 only", "STILL-CONNECTED203 AFTERNOON EIGHT-minute",
            "Actually END the eight-minute call", "HER wish",
            "NAME+BIRTHPLACE only", "FIRST134", "PAST ALLY",
            "NOT a fresh current-day political report",
            "new source mechanism requires selection rather than invention",
            "FIRST135", "BOTH parents' heritages",
            "Old39 side-clauses are NOT repaired",
            "maternal Kul NAMING to136–142", "Aadhya connection143–150",
            "Broken kavach stays BROKEN", "No infant consent",
            "Emergency action is not combat clearance",
            "Rudra does not inherit Vedic healing",
            "SIX YEARS BEFORE RUDRA'S BIRTH",
            "Cycle flaw/Devtas' indifference154–160", "Ira171–190",
            "all319 baseline files", "IMMEDIATE current-branch push BEFORE next draft",
            "Stop after Ch 135", "no136 draft or incomplete Book7 publication",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, batch)

    def test_delivered_middle_prose_keeps_forms_kul_and_pending_lore_out(self):
        prohibited = re.compile(
            r"\b(Prakriti|Dashanan|Dvandva|Sakshi|Rudhransh|Shivangi|Kaumudi|Antaraal)\b"
            r"|Unbound\s*:\s*(Swarg|Svar)|Nalin\s+Vaidya",
            re.I,
        )
        for n in (133, 134, 135):
            files = list((ROOT / "book-07").glob(f"ch-{n}-*.md"))
            self.assertLessEqual(len(files), 1, f"duplicate source {n}")
            for source in files:
                text = source.read_text(encoding="utf-8")
                with self.subTest(chapter=n):
                    self.assertIsNone(prohibited.search(text), source.name)
                    if n == 133:
                        self.assertNotRegex(text, r"(?i)\bDaksh\b")
                    if n == 134:
                        self.assertIn("Daksh", text)
                    if n == 135:
                        self.assertRegex(text, r"(?i)\bkavach\b")
                        self.assertRegex(text, r"(?i)\bdono\b")
                    self.assertEqual(text.count("### END OF CHAPTER"), 1)
                    self.assertTrue(text.endswith(f"### END OF CHAPTER {n}\n"))


if __name__ == "__main__":
    unittest.main()
