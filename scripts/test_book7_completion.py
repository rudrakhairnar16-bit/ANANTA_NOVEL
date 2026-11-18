#!/usr/bin/env python3
"""Book7 finishes140; maternal arc and later discoveries do not finish with it."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Book7CompletionTests(unittest.TestCase):
    def test_completion_authority_retains_connected_payoff_privacy_and_publication_boundaries(self):
        bible = (ROOT / "ANANTA_MASTER_BIBLE.md").read_text(encoding="utf-8")
        part = bible.split("## PART 44:", 1)[1].split("## PART 45:", 1)[0]
        for phrase in (
            "Ch139–140 ONLY", "TWO remaining Book7 chapters", "STOP140/no141 or Book8 draft",
            "maternal131–142 remains OPEN", "subtitle UNASSIGNED",
            "FIRST139", "STILL-CONNECTED215", "MORE THAN HALF", "Prakriti",
            "ALREADY PUBLIC", "no false unfamiliarity/memory loss", "Aadhya discovery before143–150",
            "ACTUALLY END215", "FIRST140", "ACTUALLY END216", "FIRST141",
            "NAME+BIRTHPLACE ONLY", "Mother–R PRIVATE", "ACTUAL contact",
            "Public213 report forwarding only to Mother", "213 inquiry job ACTUALLY CLOSED138",
            "final liability/property/repair account OPEN", "SIX YEARS BEFORE RUDRA'S BIRTH",
            "Emergency action is not combat clearance", "Rudra does not inherit Vedic healing",
            "Broken kavach stays BROKEN", "all335 baseline paths", "IMMEDIATE current-branch push",
            "reviewed explicitly numbered PR to main", "Independently export EXACT committed tree",
            "Empty remote CI is not a pass", "PR creation is not publication", "ACTUAL main tree",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, part)

    def test_delivered_last_chapters_pay_their_hooks_without_later_names_forms_or_shared_lineage_relay(self):
        forbidden = re.compile(
            r"\b(Dashanan|Dvandva|Sakshi|Rudhransh|Shivangi|Kaumudi|Antaraal)\b"
            r"|Unbound\s*:\s*(Swarg|Svar)|Nalin\s+Vaidya", re.I,
        )
        for n, opening in ((139, '"Prakriti," Rukmini said.'), (140, '"Haan," Rukmini said.')):
            files = list((ROOT / "book-07").glob(f"ch-{n}-*.md"))
            self.assertLessEqual(len(files), 1, f"duplicate source {n}")
            for p in files:
                text = p.read_text(encoding="utf-8")
                with self.subTest(chapter=n):
                    body = text.split("---", 2)[2].lstrip()
                    self.assertTrue(body.startswith(opening), p.name)
                    self.assertIsNone(forbidden.search(text), p.name)
                    self.assertEqual(text.count("### END OF CHAPTER"), 1)
                    self.assertTrue(text.endswith(f"### END OF CHAPTER {n}\n"))
                    for paragraph in text.split("\n\n"):
                        self.assertFalse(re.search(r"\bAadhya\b", paragraph, re.I) and
                                         re.search(r"\bPrakriti\b", paragraph, re.I), p.name)


if __name__ == "__main__":
    unittest.main()
