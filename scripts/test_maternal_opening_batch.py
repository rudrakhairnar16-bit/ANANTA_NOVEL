#!/usr/bin/env python3
"""Bound130–132: culture closure and first-person maternal core, not later gates."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MaternalOpeningBatchTests(unittest.TestCase):
    def test130_132_authority_is_bounded_and_does_not_renew_old_jobs(self):
        bible = (ROOT / "ANANTA_MASTER_BIBLE.md").read_text(encoding="utf-8")
        batch = bible.split("## PART 41:", 1)[1].split("## PART 42:", 1)[0]
        for phrase in (
            "Ch 130–132 only", "130 CLOSES", "131–132 OPEN",
            "FIRST130 A actually listens", "ACTUAL184 observations",
            "not proof nobody heard him", "NO maternal-origin answer before131",
            "FIRST131 Rukmini herself", "born and raised in Swarg/Svar",
            "birth name Sampoorna", "HER chosen first-person account",
            "EXILED", "OWN sister's FALSE accusations", "Highest Lord",
            "NO maternal-origin answer before131",
            "Aadhya connection143–150 remains separate",
            "maternal Kul naming and Daksh/current-power reporting",
            "no ended hired crew renewed", "remains OPEN",
            "Emergency action is not combat clearance",
            "Rudra does not inherit Vedic healing",
            "SIX YEARS BEFORE RUDRA'S BIRTH", "all311 baseline files",
            "Cycle flaw/Devtas' indifference154–160", "Ira171–190",
            "IMMEDIATE current-branch push BEFORE next draft",
            "Stop after Ch 132", "no133 draft or incomplete Book7 publication",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, batch)

    def test_delivered_prose_keeps_deferred_names_forms_and_ancestry_out(self):
        # These stricter BATCH boundaries supplement, never relax, canon_check.py.
        # Pending files are checked as each individual chapter is delivered.
        prohibited = re.compile(
            r"\b(Daksh|Prakriti|Dashanan|Dvandva|Sakshi|Rudhransh|Shivangi|Kaumudi|Antaraal)\b"
            r"|Unbound\s*:\s*(Swarg|Svar)|Nalin\s+Vaidya",
            re.I,
        )
        for n in (130, 131, 132):
            files = list((ROOT / "book-07").glob(f"ch-{n}-*.md"))
            self.assertLessEqual(len(files), 1, f"duplicate chapter source {n}")
            for source in files:
                text = source.read_text(encoding="utf-8")
                with self.subTest(chapter=n):
                    self.assertIsNone(prohibited.search(text), source.name)
                    if n == 130:
                        self.assertNotRegex(text, r"(?i)\bSamp[ou]+rna\b")
                    else:
                        self.assertIn("Sampoorna", text)
                        self.assertIn("Swarg", text)
                    self.assertEqual(text.count("### END OF CHAPTER"), 1)
                    self.assertTrue(text.endswith(f"### END OF CHAPTER {n}\n"))


if __name__ == "__main__":
    unittest.main()
