#!/usr/bin/env python3
"""Bound the authorized124–126 hearing without widening any later reveal."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SwargSourceBatchTests(unittest.TestCase):
    def test124_126_preserves_corrected_source_basis_and_finite_scope(self):
        bible = (ROOT / "ANANTA_MASTER_BIBLE.md").read_text(encoding="utf-8")
        batch = bible.split("## PART 39:", 1)[1].split("## PART 40:", 1)[0]
        for phrase in (
            "Ch 124–126 only", "six years before Rudra's birth",
            "Adhira told Ram during the old encounter",
            "not invented verbatim enemy dialogue, a new witness/document/device or Ram's independent all-seven-Loka verification",
            "still-connected short day184", "EACH person's choice",
            "entry AND return verification", "eleven-person job is CLOSED",
            "Emergency action is not combat clearance",
            "Rudra does not inherit Vedic healing", "all295 repaired baseline files",
            "Rukmini's origin/alias/exile/sister131–142",
            "full Cycle doctrine154–160", "No villain POV",
            "IMMEDIATE current-branch push BEFORE next draft",
            "Stop after Ch 126", "no127 draft or incomplete Book7 publication",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, batch)

    def test124_126_place_and_basic_report_do_not_release_later_names_or_forms(self):
        checker = ROOT / "scripts" / "canon_check.py"
        for n in (124, 125, 126):
            for allowed, text in (
                (True, "Swarg Svar Devta Kaal Divine Cycle Unbound: Pataal"),
                (False, "Sampoorna Sampurna Unbound: Swarg Daksh Dashanan Dvandva Sakshi Rudhransh"),
            ):
                with self.subTest(chapter=n, allowed=allowed):
                    with tempfile.TemporaryDirectory(prefix="ananta-source-scope-") as tmp:
                        p = Path(tmp) / f"ch-{n}-probe.md"
                        p.write_text(text + f"\n\n### END OF CHAPTER {n}\n", encoding="utf-8")
                        result = subprocess.run([sys.executable, "-B", str(checker), tmp], capture_output=True, text=True, check=False)
                    if allowed:
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    else:
                        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                        for term in ("Sampoorna", "Sampurna", "Unbound: Swarg", "Daksh", "Dashanan", "Dvandva", "Sakshi", "Rudhransh"):
                            self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)


if __name__ == "__main__":
    unittest.main()
