#!/usr/bin/env python3
"""Regression checks for the authorized Saga 4/5 chronology repair.

Run: python3 -B -m unittest discover -s scripts -p 'test_*.py' -v
These check active chronology and the bounded Ira approval, not pending lore/names.
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

    def test_ira_core_approved_other_proposals_not_activated(self):
        self.assertIn("Ira Mishra", self.bible)
        self.assertIn("Sarokaar belonging", self.bible)
        self.assertIn("Sakshi Kul", self.bible)
        self.assertIn("unknown to the characters until Ch 187–188", self.bible)
        self.assertIn("## PART 14: IRA CORE REVEAL", self.bible)
        for name in ("Nalin Vaidya", "Kaumudi", "Antaraal"):
            with self.subTest(name=name):
                self.assertNotIn(name, self.bible)
        target = ROOT / "continuity-notes" / "saga-04-repair-and-ira-reveal-proposal.md"
        self.assertTrue(target.is_file())

    def test_ira_reveal_and_choice_windows_are_explicit(self):
        self.assertIn("Ch 187–188: **IRA'S SAKSHI KUL REVEAL.**", self.saga4)
        self.assertIn("Ch 189–190: **THE CHOICE AFTER THE ANSWER.**", self.saga4)
        self.assertIn("Enough proof remains", self.saga4)
        self.assertIn("Only the Ira witness-lineage core", self.bible)

    def test_later_explicit_batch_does_not_unlock_lore(self):
        batch = self.bible.split("## PART 15:", 1)[1].split("## PART 16:", 1)[0]
        self.assertIn("Ch 62–64 only", batch)
        self.assertIn("Stop after Ch 64", batch)
        self.assertIn("all other reveal gates remain unchanged", batch)

    def test_next_bounded_batch_preserves_split_and_recovery(self):
        batch = self.bible.split("## PART 16:", 1)[1].split("## PART 17:", 1)[0]
        self.assertIn("Ch 65–67 only", batch)
        self.assertIn("66–73 multiple-city defense/team split", batch)
        self.assertIn("not permission to skip recovery", batch)
        self.assertIn("Stop after Ch 67", batch)
        self.assertIn("Pending names/lore remain pending", batch)

    def test_through70_batch_preserves_limits_and_later_reveals(self):
        batch = self.bible.split("## PART 17:", 1)[1].split("## PART 18:", 1)[0]
        self.assertIn("Ch 68–70 only", batch)
        self.assertIn("Stop after Ch 70", batch)
        self.assertIn("66–73 multiple-city defense arc", batch)
        self.assertIn("emergency action is not retroactive combat clearance", batch)
        self.assertIn("full kavach shatter before79", batch)
        self.assertIn("Pending names/lore remain pending", batch)

    def test_through73_closes_only_regional_defense_with_care_limits(self):
        batch = self.bible.split("## PART 18:", 1)[1].split("## PART 19:", 1)[0]
        self.assertIn("Ch 71–73 only", batch)
        self.assertIn("approved66–73 multiple-city defense arc", batch)
        self.assertIn("No tournament before74", batch)
        self.assertIn("light duty is not combat clearance", batch)
        self.assertIn("post48h reassessment", batch)
        self.assertIn("Pending names/lore remain pending", batch)
        self.assertIn("Stop after Ch 73", batch)

    def test_single74_opens_tournament_without_resetting_medical_cliff(self):
        continuation = self.bible.split("## PART 19:", 1)[1].split("## PART 20:", 1)[0]
        self.assertIn("Ch 74 only", continuation)
        self.assertIn("already-approved74–78 tournament arc", continuation)
        self.assertIn("medical alarm first", continuation)
        self.assertIn("spectator permission is not permission to fight", continuation)
        self.assertIn("no full shatter before79 or origin answer before81", continuation)
        self.assertIn("Stop after Ch 74", continuation)

    def test_three_chapter_default_and75_77_preserve_story_gates(self):
        standing = self.bible.split("### 12.7 ", 1)[1].split("## PART 13:", 1)[0]
        batch = self.bible.split("## PART 20:", 1)[1].split("## PART 21:", 1)[0]
        self.assertIn("Three chapters per batch", standing)
        self.assertIn("three chapters per batch", batch)
        self.assertIn("Ch 75–77 only", batch)
        self.assertIn("falling injured porter immediately", batch)
        self.assertIn("spectator permission is not combat clearance", batch)
        self.assertIn("no full kavach shatter before79", batch)
        self.assertIn("no father-origin answer before81", batch)
        self.assertIn("Stop after Ch 77", batch)

    def test78_80_closes_book4_without_early_origin_or_mastery(self):
        batch = self.bible.split("## PART 21:", 1)[1].split("## PART 22:", 1)[0]
        self.assertIn("Ch 78–80 only", batch)
        self.assertIn("No full shatter in78", batch)
        self.assertIn("actual complete loss", batch)
        self.assertIn("true signature exposed to all Lokas", batch)
        self.assertIn("No father-origin answer before81", batch)
        self.assertIn("no villain POV", batch)
        self.assertIn("not a new Swaroop", batch)
        self.assertIn("Stop after Ch 80", batch)


    def test81_83_opens_only_paternal_core_with_no_cost_reset(self):
        batch = self.bible.split("## PART 22:", 1)[1].split("## PART 23:", 1)[0]
        for phrase in (
            "Ch 81–83 only", "81–92 father-origin reveal",
            "Ram / Daavansh, Pataal, Asuran Kul",
            "Maternal origin remains gated", "No villain POV",
            "No realm visit before93", "inherited Vedic healing",
            "Book5 subtitle unassigned", "Stop after Ch 83",
        ):
            self.assertIn(phrase, batch)


    def test84_86_keeps_paternal_truth_and2020_inside_later_gates(self):
        batch = self.bible.split("## PART 23:", 1)[1].split("## PART 24:", 1)[0]
        for phrase in (
            "Ch 84–86 only", "81–92 father-origin arc remains open",
            "Yeh hukm kisne diya tha?", "supra-Kul Loka authority",
            "Devta/Maha Devta111", "2020 defeat of Adhira",
            "before2020", "Ram's private manipulator knowledge stays private",
            "Kaal119", "lived household years", "no villain POV",
            "No realm visit before93", "Stop after Ch 86",
        ):
            self.assertIn(phrase, batch)


    def test87_89_continues_history_without_early_journey_or_inherited_cure(self):
        batch = self.bible.split("## PART 24:", 1)[1].split("## PART 25:", 1)[0]
        for phrase in (
            "Ch 87–89 only", "81–92 father-origin arc",
            "Aap mujhe Pataal dikhaayenge?", "No realm visit before93",
            "Vedic upbringing / learned healing",
            "Rudra does not inherit Vedic healing",
            "each friend's right to choose", "Devta/Maha Devta111",
            "Kaal119", "Ram's private manipulator knowledge stays private",
            "villain POV", "Stop after Ch 89",
        ):
            self.assertIn(phrase, batch)


    def test90_92_closes_paternal_arc_without_early_visit_or_absolution(self):
        batch = self.bible.split("## PART 25:", 1)[1].split("## PART 26:", 1)[0]
        for phrase in (
            "Ch 90–92 only", "81–92 father-origin arc",
            "invitation to Veer immediately", "each friend's right to choose",
            "Rudra does not inherit Vedic healing",
            "automatic forgiveness", "No realm visit before93",
            "Devta/Maha Devta111", "Kaal119",
            "Ram's private manipulator knowledge stays private",
            "villain POV", "Stop after Ch 92",
        ):
            self.assertIn(phrase, batch)


    def test93_95_uses_approved_passage_and_actual_visit_without_early_power(self):
        batch = self.bible.split("## PART 26:", 1)[1].split("## PART 27:", 1)[0]
        for phrase in (
            "Ch 93–95 only", "93–97 Pataal visit arc",
            "Mentor-verified passage", "an old natural passage",
            "entry and return verified by existing mentors",
            "No new device, blood-key or travel power",
            "actual Pataal crossing within93–95",
            "individual reassessment", "informed choice",
            "Mentor backstories97–102", "Devta/Maha Devta111",
            "Kaal119", "villain POV", "Stop after Ch 95",
        ):
            self.assertIn(phrase, batch)


    def test96_98_finishes_visit_and_opens_only_existing_mentor_history(self):
        batch = self.bible.split("## PART 27:", 1)[1].split("## PART 28:", 1)[0]
        for phrase in (
            "Ch 96–98 only", "Father81–92 is CLOSED",
            "actually crossed in93 and returned in95",
            "No mentor backstory before97", "mentor backstories97–102",
            "Vedant as Ram's former student", "shared-guru identity",
            "individual post-visit reassessments",
            "Rudra does not inherit Vedic healing",
            "attacks103–110", "Devta/Maha Devta111", "Kaal119",
            "villain POV", "Stop after Ch 98",
        ):
            self.assertIn(phrase, batch)


    def test99_101_crosses_book_boundary_without_closing_mentor_arc_early(self):
        batch = self.bible.split("## PART 28:", 1)[1].split("## PART 29:", 1)[0]
        for phrase in (
            "Ch 99–101 only", "Book5 ends100; Book6 starts101",
            "mentor backstories97–102", "mentor arc remains OPEN at101",
            "20 exact numeric sources once/END-stripped",
            "FREEZE it before101", "individual clinical reviews",
            "Rudra does not inherit Vedic healing",
            "attacks103–110", "Devta/Maha Devta111", "Kaal119",
            "villain POV", "Stop after Ch 101",
        ):
            self.assertIn(phrase, batch)


    def test102_104_closes_mentors_and_opens_only_pataal_attack_arc(self):
        batch = self.bible.split("## PART 29:", 1)[1].split("## PART 30:", 1)[0]
        for phrase in (
            "Ch 102–104 only", "Mentor arc closes at102",
            "No attacks before103", "attacks103–110 in Pataal",
            "whole103–110 arc remains OPEN at104",
            "No second expedition is already agreed", "entry AND return",
            "individual clinical assessments", "not combat clearance",
            "Rudra does not inherit Vedic healing", "Book5 freeze",
            "Devta/Maha Devta111", "Kaal119", "villain POV",
            "Stop after Ch 104",
        ):
            self.assertIn(phrase, batch)



    def test105_107_continues_flight_and_care_without_closing_attack_arc(self):
        batch = self.bible.split("## PART 30:", 1)[1].split("## PART 31:", 1)[0]
        for phrase in (
            "Ch 105–107 only", "attack arc remains OPEN at107",
            "The spear left his hand towards the driver holding the door.",
            "all eleven party members are already Earth-side",
            "vehicles have NOT departed", "ACTUAL urgent assessment",
            "entry AND return verification", "Atala/Sutala were heard labels",
            "Rudra does not inherit Vedic healing", "Book5 freeze",
            "Devta/Maha Devta111", "Kaal119", "no villain POV",
            "Stop after Ch 107",
        ):
            self.assertIn(phrase, batch)


    def test108_110_resolves_rolling_timber_and_closes_only_current_raid(self):
        batch = self.bible.split("## PART 31:", 1)[1].split("## PART 32:", 1)[0]
        for phrase in (
            "Ch 108–110 only", "attacks103–110 in Pataal",
            "The baulk began to roll towards her back.",
            "six-person rescue group inside", "four people outside",
            "original four patients remain in Mirzapur",
            "care is not conditional on innocence", "Close this103–110 attack block by110",
            "Entry AND return verification", "Atala/Sutala remain heard labels",
            "Rudra does not inherit Vedic healing", "Book5 freeze",
            "Devta/Maha Devta111", "Kaal119", "No villain POV",
            "Stop after Ch 110",
        ):
            self.assertIn(phrase, batch)


    def test111_113_opens_only_prepared_control_and_approved_threat_arc(self):
        batch = self.bible.split("## PART 32:", 1)[1]
        for phrase in (
            "Ch 111–113 only", "111–118 Unbound:Pataal / Maha Devta-level battle arc",
            "Haath khulne se pehle", "same day97 evening",
            "Forward elapsed weeks require actual recovery",
            "Emergency action is not combat clearance",
            "a clear line BEYOND the target", "My hand opened. The work did not stop.",
            "Full concealing kavach remains lost", "Rudra does not inherit Vedic healing",
            "attacks103–110 are CLOSED", "Devta/Maha Devta titles unlock at111",
            "unnamed, externally shown threat", "entry AND return verification",
            "Kaal119–120", "Book5 freeze", "Stop after Ch 113",
        ):
            self.assertIn(phrase, batch)


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

    def test_ira_birth_lineage_name_stays_gated_until187(self):
        self.assert_gate("Sakshi Kul", 186, 187)
        early = self.run_checker([(61, "Sakshi")])
        self.assertNotEqual(early.returncode, 0, early.stdout + early.stderr)
        self.assertIn("PLACEMENT LEAK", early.stdout)

    def test_other_origin_and_antagonist_gates_unchanged(self):
        for term, before, at in (
            ("Asuran", 80, 81),
            ("Swarg", 130, 131),
            ("Kaal", 118, 119),
            ("Dashanan", 178, 179),
        ):
            with self.subTest(term=term):
                self.assert_gate(term, before, at)

    def test_pataal_release_does_not_release_later_hierarchy_or_fusion(self):
        for term, before, at in (
            ("Pataal", 80, 81),
            ("Maha Devta", 110, 111),
            ("Dvandva", 130, 131),
        ):
            with self.subTest(term=term):
                self.assert_gate(term, before, at)

    def test2020_flashback_release_does_not_move_divine_title_gate(self):
        self.assert_gate("Adhira", 80, 81)
        self.assert_gate("Devta", 110, 111)

    def test_next_father_batch_does_not_release_later_names(self):
        for number in (87, 88, 89):
            result = self.run_checker([(number, "Devta Kaal Swarg Sakshi")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Devta", "Kaal", "Swarg", "Sakshi"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

    def test_paternal_arc_close_does_not_release_later_names(self):
        for number in (90, 91, 92):
            result = self.run_checker([(number, "Devta Kaal Swarg Sakshi")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Devta", "Kaal", "Swarg", "Sakshi"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

    def test_first_pataal_visit_does_not_release_later_names(self):
        for number in (93, 94, 95):
            result = self.run_checker([(number, "Devta Kaal Swarg Sakshi")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Devta", "Kaal", "Swarg", "Sakshi"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

    def test_mentor_backstories_do_not_release_later_names(self):
        for number in (96, 97, 98):
            result = self.run_checker([(number, "Devta Kaal Swarg Sakshi")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Devta", "Kaal", "Swarg", "Sakshi"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

    def test_book_boundary_does_not_release_later_names(self):
        for number in (99, 100, 101):
            result = self.run_checker([(number, "Devta Kaal Swarg Sakshi")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Devta", "Kaal", "Swarg", "Sakshi"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

    def test_attack_arc_does_not_release_principal_or_later_names(self):
        for number in (102, 103, 104):
            result = self.run_checker([(number, "Devta Kaal Swarg Sakshi")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Devta", "Kaal", "Swarg", "Sakshi"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

    def test_continued_attack_batch_keeps_later_reveal_names_gated(self):
        for number in (105, 106, 107):
            result = self.run_checker([(number, "Devta Kaal Swarg Sakshi")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Devta", "Kaal", "Swarg", "Sakshi"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

    def test_attack_arc_closure_does_not_release111_or_later_names(self):
        for number in (108, 109, 110):
            result = self.run_checker([(number, "Devta Kaal Swarg Sakshi")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Devta", "Kaal", "Swarg", "Sakshi"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

    def test111_113_releases_rank_titles_not_later_names(self):
        for number in (111, 112, 113):
            released = self.run_checker([(number, "Devta Maha Devta")])
            self.assertEqual(released.returncode, 0, released.stdout + released.stderr)
            result = self.run_checker([(number, "Kaal Swarg Sakshi Dvandva")])
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            for term in ("Kaal", "Swarg", "Sakshi", "Dvandva"):
                self.assertIn(f"PLACEMENT LEAK '{term}'", result.stdout)

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
