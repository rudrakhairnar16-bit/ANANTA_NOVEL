#!/usr/bin/env python3
"""Keep the approved127–129 cultural breather local and later reveals locked."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SwargCultureBatchTests(unittest.TestCase):
    def test127_129_has_finite_scope_and_observed_culture_not_new_lore(self):
        bible = (ROOT / "ANANTA_MASTER_BIBLE.md").read_text(encoding="utf-8")
        batch = bible.split("## PART 40:", 1)[1].split("## PART 41:", 1)[0]
        for phrase in (
            "Ch 127–129 only", "127–130 realm-culture / daily-life breather",
            "still-connected SHORT day186 R+S call",
            "receiver handled that queue/referral",
            "Actually END the call", "121–126 journey/source-access is CLOSED",
            "not a new divine caste/rank system", "No villain POV",
            "EACH person's current review/actual functional trial/choice",
            "entry AND return verification", "deposit deductedONCE",
            "Emergency action is not combat clearance",
            "Rudra does not inherit Vedic healing",
            "maternal origin/alias/exile/sister131–142",
            "Cycle flaw/Devtas' indifference154–160", "Ira171–190",
            "SIX YEARS BEFORE RUDRA'S BIRTH", "all303 baseline files",
            "IMMEDIATE current-branch push BEFORE next draft",
            "Stop after Ch 129", "no130 draft or incomplete Book7 publication",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, batch)

    def test127_129_culture_does_not_release_maternal_names_forms_or_ancestry(self):
        checker = ROOT / "scripts" / "canon_check.py"
        for n in (127, 128, 129):
            for allowed, text in (
                (True, "Swarg Svar Devta Kaal Divine Cycle Unbound: Pataal"),
                (False, "Sampoorna Sampurna Unbound: Swarg Daksh Dashanan Dvandva Sakshi Rudhransh"),
            ):
                with self.subTest(chapter=n, allowed=allowed):
                    with tempfile.TemporaryDirectory(prefix="ananta-culture-scope-") as tmp:
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
