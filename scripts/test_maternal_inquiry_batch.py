#!/usr/bin/env python3
"""Bound136–138: adult agency and a newly approved public inquiry, not backfill."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MaternalInquiryBatchTests(unittest.TestCase):
    def test136_138_uses_selected_fresh_source_and_preserves_private_and_later_gates(self):
        bible = (ROOT / "ANANTA_MASTER_BIBLE.md").read_text(encoding="utf-8")
        batch = bible.split("## PART 43:", 1)[1].split("## PART 44:", 1)[0]
        for phrase in (
            "Ch 136–138 only", "fresh_bounded_inquiry",
            "CURRENT care/consent", "entry AND return",
            "SAME Swarg counter / PUBLIC ruler-status question",
            "NO new important name, secret archive, power or private family-history leak",
            "NO retrospective observation/backfill or old-file rewrite",
            "FIRST136", "STILL-CONNECTED209 AFTERNOON EIGHT-minute",
            "ACTUALLY END209 call", "not universal emergency veto",
            "NAME+BIRTHPLACE only", "Mother–R PRIVATE",
            "FIRST137", "No injured carrier or patient route-test",
            "FIRST138", "current institutional testimony AS OF THIS inquiry",
            "Actually RETURN", "deposit deducted ONCE",
            "ALL workers LEAVE", "remains OPEN",
            "maternal Kul NAMING139–142", "Aadhya connection143–150 unchanged",
            "Emergency action is not combat clearance",
            "Rudra does not inherit Vedic healing", "Broken kavach stays BROKEN",
            "SIX YEARS BEFORE RUDRA'S BIRTH",
            "Cycle flaw/Devtas' indifference154–160/Ira171–190",
            "all327 baseline files", "IMMEDIATE current-branch push BEFORE next draft",
            "Stop after Ch 138", "no139 draft or incomplete Book7 publication",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, batch)

    def test_delivered_inquiry_prose_keeps_deferred_lineage_names_and_forms_out(self):
        prohibited = re.compile(
            r"\b(Prakriti|Dashanan|Dvandva|Sakshi|Rudhransh|Shivangi|Kaumudi|Antaraal)\b"
            r"|Unbound\s*:\s*(Swarg|Svar)|Nalin\s+Vaidya",
            re.I,
        )
        for n in (136, 137, 138):
            files = list((ROOT / "book-07").glob(f"ch-{n}-*.md"))
            self.assertLessEqual(len(files), 1, f"duplicate source {n}")
            for source in files:
                text = source.read_text(encoding="utf-8")
                with self.subTest(chapter=n):
                    self.assertIsNone(prohibited.search(text), source.name)
                    if n == 137:
                        self.assertNotRegex(text, r"(?i)\bDaksh\b")
                    if n == 138:
                        self.assertIn("Daksh", text)
                    self.assertEqual(text.count("### END OF CHAPTER"), 1)
                    self.assertTrue(text.endswith(f"### END OF CHAPTER {n}\n"))


if __name__ == "__main__":
    unittest.main()
