#!/usr/bin/env python3
"""Regression checks for the authorized Saga 4/5 chronology repair.

Run: python3 -B -m unittest discover -s scripts -p 'test_*.py' -v
These check the active outline/checker contract, not the pending Ira proposal.
"""

from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BIBLE = ROOT / "ANANTA_MASTER_BIBLE.md"
CHECKER = ROOT / "scripts" / "canon_check.py"


class OutlineChronologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bible = BIBLE.read_text(encoding="utf-8")
        cls.saga4 = cls.bible.split("### ═══ BOOKS 10–12:", 1)[1].split(
            "### ═══ BOOKS 13–15:", 1
        )[0]
        cls.saga5 = cls.bible.split("### ═══ BOOKS 13–15:", 1)[1].split(
            "## PART 5:", 1
        )[0]
        cls.contract = cls.bible.split("### 13.1 ", 1)[1].split(
            "### 13.2 ", 1
        )[0]
        cls.events = {
            event.strip(): (int(start), int(end))
            for event, start, end in re.findall(
                r"^\| ([^|]+) \| (\d+)–(\d+) \|", cls.contract, re.M
            )
        }

    def test_existing_marriage_and_pregnancy_slots_stay(self):
        self.assertEqual(self.events["Marriage"], (217, 219))
        self.assertEqual(self.events["Pregnancy confirmation"], (220, 222))

    def test_gestation_birth_separation_reunion_training_order(self):
        names = [
            "Adult-team preparation",
            "Marriage",
            "Pregnancy confirmation",
            "War and gestation",
            "Birth and recovery",
            "Separation",
            "Return and reunion",
            "Bonding and first direct guidance",
        ]
        for before, after in zip(names, names[1:]):
            with self.subTest(before=before, after=after):
                self.assertLess(self.events[before][1], self.events[after][0])
        self.assertEqual(self.events["Birth and recovery"], (230, 232))
        self.assertEqual(self.events["Separation"], (233, 240))
        self.assertEqual(self.events["Return and reunion"], (241, 243))
        self.assertEqual(
            self.events["Bonding and first direct guidance"], (244, 248)
        )

    def test_key_outline_matches_contract_not_old_training_block(self):
        keys = self.saga4.split("**Key Chapters:**", 1)[1]
        repaired = [
            (int(start), int(end))
            for start, end in re.findall(r"^- Ch (\d+)–(\d+):", keys, re.M)
            if int(start) >= 211
        ]
        self.assertEqual(
            repaired,
            [(211, 216), (217, 219), (220, 222), (223, 229), (230, 232), (233, 240)],
        )
        self.assertNotIn("Training Rudhransh (who ages rapidly", self.bible)
        self.assertIn("postnatal recovery interval", self.saga4)
        self.assertIn("Months visibly pass", self.saga4)

    def test_one_reunion_and_natural_five_year_growth(self):
        self.assertIn("Saga 4 ends with the family still separated", self.saga4)
        self.assertIn("Ch 240 ends before his actual return", self.saga4)
        self.assertIn("Ch 241–243: **ACTUAL RETURN / REUNION.**", self.saga5)
        self.assertIn("five Earth years have passed", self.saga5)
        self.assertIn("2029-2034", self.bible)
        self.assertIn("counterpart Aadhya", self.saga4)
        self.assertIn("Aadhya remains alive", self.saga4)

    def test_ira_belonging_preserved_proposals_not_activated(self):
        self.assertIn("Ira Mishra", self.bible)
        self.assertIn("Sarokaar belonging", self.bible)
        self.assertIn("birth Kul remains UNKNOWN/HIDDEN", self.bible)
        self.assertIn("### 13.4 RECOMMENDATION — [PROPOSED], NOT CANON", self.bible)
        for name in ("Sakshi Kul", "Nalin Vaidya", "Kaumudi", "Antaraal"):
            with self.subTest(name=name):
                self.assertNotIn(name, self.bible)
        target = ROOT / "continuity-notes" / "saga-04-repair-and-ira-reveal-proposal.md"
        self.assertTrue(target.is_file())


class CheckerBoundaryTests(unittest.TestCase):
    def run_checker(self, chapters):
        with tempfile.TemporaryDirectory(prefix="ananta-chronology-") as tmp:
            directory = Path(tmp)
            for number, text in chapters:
                (directory / f"ch-{number:02d}-probe.md").write_text(
                    text + f"\n\n### END OF CHAPTER {number}\n", encoding="utf-8"
                )
            return subprocess.run(
                [sys.executable, "-B", str(CHECKER), str(directory)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

    def assert_gate(self, term, before, at):
        early = self.run_checker([(before, term)])
        self.assertNotEqual(early.returncode, 0, early.stdout + early.stderr)
        self.assertIn("PLACEMENT LEAK", early.stdout)
        self.assertIn(f"ch-{before:02d}-probe.md", early.stdout)
        released = self.run_checker([(at, term)])
        self.assertEqual(released.returncode, 0, released.stdout + released.stderr)
        self.assertIn(f"ch-{at:02d}-probe.md", released.stdout)

    def test_rudhransh_birth_name_gate(self):
        self.assert_gate("Rudhransh", 229, 230)

    def test_shivangi_gate_not_moved_with_rudhransh(self):
        self.assert_gate("Shivangi", 240, 241)

    def test_other_origin_and_antagonist_gates_unchanged(self):
        for term, before, at in (
            ("Asuran", 80, 81),
            ("Swarg", 130, 131),
            ("Kaal", 118, 119),
            ("Dashanan", 178, 179),
        ):
            with self.subTest(term=term):
                self.assert_gate(term, before, at)

    def test_three_digit_chapters_scanned_and_sorted_numerically(self):
        result = self.run_checker(
            [(230, "Ordinary prose."), (100, "Ordinary prose."), (99, "Ordinary prose.")]
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        rows = re.findall(r"^ch-(\d+)-probe\.md", result.stdout, re.M)
        self.assertEqual(rows, ["99", "100", "230"])

    def test_final_chapter_is_scanned_too(self):
        result = self.run_checker([(300, "A quiet ending.")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ch-300-probe.md", result.stdout)

    def test_child_age_not_subject_to_opening_nineteen_guard(self):
        result = self.run_checker([(241, "Rudhransh was 5 years old.")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("AGE mention", result.stdout)

    def test_saga1_age_guard_still_active(self):
        result = self.run_checker([(60, "Rudra was 21 years old.")])
        self.assertIn("AGE mention '21' (locked=19)", result.stdout)

    def test_hospital_answer_still_allowed_only_in59(self):
        line = "The one who broke God."
        allowed = self.run_checker([(59, line)])
        self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)
        refused = self.run_checker([(60, line)])
        self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)
        self.assertIn("DIALOGUE LOCK LEAK", refused.stdout)


if __name__ == "__main__":
    unittest.main()
