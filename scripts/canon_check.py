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
EARLY_REVEAL_BANS = [
    (r'\basuran\w*\b', "Father's Pataal origin reveal = Saga 2 (Ch 81-92)"),
    (r'\bpataal\b|\bpatala\b', "Pataal reveal = Saga 2"),
    (r'\bdashanan\b', "Kaal's real name = never in Book 1"),
    (r'\bkaal\b', "Kaal name first spoken Ch 119-120; shadow only Ch 60"),
    (r'\bardhanarishwar\w*\b', "Prologue-only term in Book 1; named reveal = Saga 3"),
    (r'\bswarg\b|\bsvar\b', "Mother's Swarg origin reveal = Saga 3 (Ch 131-142)"),
    (r'\bsutala\b', "Sutala named reveal = Saga 2+ (Prologue keeps it unnamed-ish)"),
    (r'\bloka\w*\b', "Lokas framework reveal = post-Book 1"),
    (r'\bmaha devta\w*\b|\bdevta\w*\b', "Divine hierarchy reveal = post-Book 1"),
    (r'\bswaroop\w*\b', "Swaroop = Book 3 transformation term (Ch 41-60)"),
    (r'\bj[aa]grut\b|\bdvandva\b|\banant\b', "Rudra Swaroop names = Book 3+"),
    (r'\bshakti:|\bvelum:|\bdrishti:', "Epic State names in combat = Book 3"),
    (r'\bepic state\b', "System term characters do not know in Saga 1"),
    (r'\bvedant\b|\bdhruv\b|\bsitara\b', "Mentors arrive Book 3 (Ch 41-45)"),
    (r'\brudhransh\b|\bshivangi\b', "Children = Saga 4-5 (name leak ban)"),
    (r'\badhira\b', "2020 villain = flashback-only, post-Book 1"),
    (r'\bdaksh\b', "Swarg usurper = Saga 3 antagonist"),
    (r'\bkaal chakra\b', "Ending line = Ch 300 only"),
    (r'\bthe cycle\b|\bdivine cycle\b', "Cycle as named doctrine = not spoken in Book 1 streets"),
]

# --- PLACEMENT-SPECIFIC BANS ---------------------------------------------------
PLACEMENT_BANS = [
    (r'\bkul\w*\b', 18, 'First explicit "Kul" mention = Ch 18'),
    (r'\baegis\b|\bmeridian\b', 9, 'Aegis Meridian scouts first appear = Ch 9 (name spoken even later is fine)'),
]

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

    for pat, why in GLOBAL_BANS:
        for m in re.finditer(pat, prose, re.I):
            fails.append(f"GLOBAL BAN '{m.group(0)}' — {why}")

    if not is_reference:
        for pat, why in EARLY_REVEAL_BANS:
            for m in re.finditer(pat, prose, re.I):
                fails.append(f"EARLY REVEAL '{m.group(0)}' — {why}")
        for pat, min_ch, why in PLACEMENT_BANS:
            if n < min_ch:
                for m in re.finditer(pat, prose, re.I):
                    fails.append(f"PLACEMENT LEAK '{m.group(0)}' — {why}")
        for pat in LOCK_LEAKS:
            for m in re.finditer(pat, prose, re.I):
                fails.append(f"DIALOGUE LOCK LEAK '{m.group(0)[:40]}...'")
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
    files = sorted(CHAPTER_DIR.glob('*.md'))
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
