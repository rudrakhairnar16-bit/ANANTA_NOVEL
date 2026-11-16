#!/usr/bin/env python3
"""ANANTA canon checker — word-by-word + rule-level validation per bible v9.1.

Usage: python3 scripts/canon_check.py [chapter_dir]
"""
import pathlib, re, sys

CHAPTER_DIR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('book-01-awakening')
TARGET_WORDS = 5000
LOW, HIGH = 4300, 6200  # acceptable band around ~5000

# --- GLOBAL BANS (any chapter, any era) --------------------------------------
GLOBAL_BANS = [
    (r'\bavatar\b', 'REJECTED term "Avatar/Avatar State" (bible rule 3)'),
    (r'\bneo[- ]varanasi\b', 'Futuristic city ban (rule 4)'),
    (r'\bhologram\w*\b|\bholographic\b', 'Futuristic tech ban (rule 4)'),
    (r'\bflying car\w*\b', 'Futuristic tech ban (rule 4)'),
    (r'\bmana\b', 'Western fantasy term banned (style guide)'),
    (r'\bf?elves\b|\belf\b', 'Western fantasy trope banned (style guide)'),
    (r'\bmagic wand\w*\b|\bwizards?\b', 'Western fantasy trope banned (style guide)'),
    (r'\blightsaber\w*\b|\blaser gun\w*\b|\bspaceship\w*\b', 'Sci-fi trope out of setting'),
    (r'\btime machine\w*\b', 'Out-of-setting trope (time is Kaal-domain, Saga 4+)'),
]

# --- BOOK 1 EARLY-REVEAL BANS (apply to NEW chapters 04+ only) ----------------
# Reference chapters (00-03) are locked canon prose and are exempt.
EARLY_REVEAL_BANS = []  # all rows moved to ERA_GATED (bible-scheduled reveals)

# --- PLACEMENT-SPECIFIC BANS ---------------------------------------------------
PLACEMENT_BANS = [
    (r'\bkul\w*\b', 18, 'First explicit "Kul" mention = Ch 18'),
    (r'\baegis\b|\bmeridian\b', 9, 'Aegis Meridian scouts first appear = Ch 9 (name spoken even later is fine)'),
]

# --- ERA-GATED REVEAL TABLE (user-approved Book-3 unlocking, 2026-11-14) -------
# Terms from EARLY_REVEAL_BANS that the bible unseals at specific chapters.
# n < min_ch  => still banned. Same semantics as PLACEMENT_BANS.
ERA_GATED = [
    (r'\bloka\w*\b', 41, 'Lokas framework reveal = Book 3 (Ch 41+)'),
    (r'\bsutala\b', 46, "Sutala named = Ira's siege revelation (Ch 46+)"),
    (r'\bswaroop\w*\b', 51, 'Swaroop term = attempts arc (Ch 51+)'),
    (r'\bvedant\b|\bdhruv\b|\bsitara\b', 41, 'Mentors arrive Book 3 (Ch 41-45)'),
    (r'\bshakti:|\bvelum:|\bdrishti:', 51, 'Epic State names in combat = Ch 51+'),
    (r'\bepic state\b', 51, 'System term = Ch 51+'),
    (r'\bj[aa]grut\b', 56, "Rudra's first Swaroop name = Ch 56"),
    (r'\bthe one who broke god\b', 59, "Ram's hospital line = Ch 59"),
    (r'\bardhanarishwar\w*\b', 60, 'Ch-60 rooftop whisper only; named reveal = Saga 3'),
    (r'\bthe cycle\b|\bdivine cycle\b', 60, 'Ch-60 whisper only; doctrine naming = later'),
    (r'\basuran\w*\b', 81, "Father's Pataal origin reveal = Saga 2 (Ch 81-92)"),
    (r'\bpataal\b|\bpatala\b', 81, 'Pataal reveal = Saga 2 (Ch 81-92)'),
    (r'\badhira\b', 81, '2020 villain = flashback-only, Saga 2+'),
    (r'\bmaha devta\w*\b|\bdevta\w*\b', 111, 'Maha Devta-level threat = Ch 111-118'),
    (r'\bkaal\b', 119, 'Kaal name first spoken Ch 119-120; shadow only Ch 60'),
    (r'\bswarg\b|\bsvar\b', 131, "Mother's Swarg origin reveal = Saga 3 (Ch 131-142)"),
    (r'\bdaksh\b', 131, 'Swarg usurper = Saga 3 antagonist'),
    (r'\bdashanan\b', 179, "Kaal's real name = Saga 3+ territory"),
    (r'\bdvandva\b', 131, 'Dual-realm fusion = Saga 3 (Ch 143+)'),
    (r'\bsakshi\b', 187, 'Approved Ira birth-Kul name = Ch 187-188, Part 14'),
    (r'\banant\b', 241, 'Late Swaroop name = Saga 4+'),
    (r'\brudhransh\b', 230, 'Birth = Saga 4 Ch 230-232; chronology repair Part 13'),
    (r'\bshivangi\b', 241, 'Existing Shivangi name gate unchanged (Saga 4-5)'),
    (r'\bkaal chakra\b', 300, 'Ending line = Ch 300 only'),
]

# EARLY_REVEAL rows NO LONGER live here once era-gated; the plain list retains
# only terms with no scheduled reveal (eternal bans handled above in GLOBAL).

# --- VERBATIM LOCKS that must NOT leak early ----------------------------------
LOCK_LEAKS = [
    r'so the asuran prince lives',          # Ch 31-34
    r'i created your gods',                 # Ch 179-180
    r'the one who broke god',               # Ch 59
    r'it\'s starting\. everything i trained you for',  # Ch 20 (allowed only AT ch 20)
    r'main tere ant ke liye khud aaunga',   # Lock 4: Prologue or Saga 3 only
    r'rukho?.*divine cycle.*mat banao',     # Ch 300 ending
]

AGE_GUARD = re.compile(r'\b(\d{1,2})[- ]years?[- ]old\b|\bage[d]?\s+(\d{1,2})\b', re.I)

def strip_meta(text: str) -> str:
    """Remove YAML front matter and agent continuity notes; return prose only."""
    text = re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)
    idx = text.find('### END OF CHAPTER')
    if idx != -1:
        text = text[:idx]
    return text

def scan_file(path: pathlib.Path, is_reference: bool):
    raw = path.read_text(encoding='utf-8')
    prose = strip_meta(raw)
    words = len(prose.split())
    fails, warns = [], []

    def chap_num():
        m = re.match(r'ch-(\d+)', path.name)
        return int(m.group(1)) if m else 0

    n = chap_num()

    # Chapter-scoped allowances for bible-LOCKED lines delivered at their chapter.
    # Ch 17 entity dying lock: "You don't even know what you are, Asuran child."
    # Mask the locked phrase before running the early-reveal bans on this chapter.
    if n == 17:
        prose = re.sub(r'\basuran child\b', 'LOCKPHRASE7', prose, flags=re.I)
    if n == 20:
        prose = re.sub(r"it's starting\. everything i trained you for\. everything i was afraid of",
                       'LOCKPHRASE20', prose, flags=re.I)
    # Ch 31-34 whisper lock release (Bible Part 12.5, user-approved 2026-11-14):
    # the Prologue Lord's line "So the Asuran prince lives" is sanctioned ONLY
    # inside this arc; it remains banned everywhere else.
    if n in (31, 32, 33, 34):
        prose = re.sub(r'so the asuran prince lives', 'LOCKPHRASE31_34', prose, flags=re.I)

    for pat, why in GLOBAL_BANS:
        for m in re.finditer(pat, prose, re.I):
            fails.append(f"GLOBAL BAN '{m.group(0)}' — {why}")

    if not is_reference:
        for pat, why in EARLY_REVEAL_BANS:
            for m in re.finditer(pat, prose, re.I):
                fails.append(f"EARLY REVEAL '{m.group(0)}' — {why}")
        for pat, min_ch, why in PLACEMENT_BANS + ERA_GATED:
            if n < min_ch:
                for m in re.finditer(pat, prose, re.I):
                    fails.append(f"PLACEMENT LEAK '{m.group(0)}' — {why}")
        LOCK_ALLOW = {59: r'the one who broke god'}
        for pat in LOCK_LEAKS:
            for m in re.finditer(pat, prose, re.I):
                if n in LOCK_ALLOW and re.match(LOCK_ALLOW[n], pat):
                    continue
                fails.append(f"DIALOGUE LOCK LEAK '{m.group(0)[:40]}...'")
        # The nineteen-year baseline is scoped to Saga 1-3. Later chapters
        # include elapsed years and children; ages follow the Part 13 ledger.
        if n <= 180:
            for m in AGE_GUARD.finditer(prose):
                num = m.group(1) or m.group(2)
                if num and int(num) != 19:
                    ctx = prose[max(0, m.start()-60):m.end()+40].replace('\n', ' ')
                    warns.append(f"AGE mention '{num}' (locked=19): ...{ctx}...")
    else:
        pass  # reference prose is locked canon; global bans still applied above

    if not is_reference and n not in (0,):
        if words < LOW or words > HIGH:
            warns.append(f"WORD COUNT {words} outside {LOW}-{HIGH} band (target ~{TARGET_WORDS})")

    return words, fails, warns

def main():
    files = sorted(
        (f for f in CHAPTER_DIR.glob('*.md') if re.match(r'^ch-\d{2,3}-', f.name)),
        key=lambda f: int(re.match(r'^ch-(\d+)', f.name).group(1)),
    )
    if not files:
        print('No chapter files found.'); sys.exit(1)
    total_fails = 0
    print(f"{'FILE':42} {'WORDS':>6}  {'RESULT'}")
    print('-' * 78)
    for f in files:
        is_ref = f.name[:5] in ('ch-00', 'ch-01', 'ch-02', 'ch-03')
        words, fails, warns = scan_file(f, is_ref)
        status = 'PASS' if not fails else 'FAIL'
        if warns and not fails:
            status = 'PASS (warn)'
        total_fails += len(fails)
        print(f"{f.name:42} {words:>6}  {status}")
        for x in fails:
            print(f"    ❌ FAIL: {x}")
        for x in warns:
            print(f"    ⚠️  WARN: {x}")
    print('-' * 78)
    print('RESULT:', 'ALL PASS ✅' if total_fails == 0 else f'{total_fails} FAIL(ES) ❌')
    sys.exit(1 if total_fails else 0)

if __name__ == '__main__':
    main()
