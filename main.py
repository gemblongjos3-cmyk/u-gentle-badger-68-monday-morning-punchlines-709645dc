#!/usr/bin/env python3
"""Pick the best one-liner from a shortlist and write it to /output/entry.txt.

Contest: "Monday Morning Punchlines" (make.fun, slug
u-gentle-badger-68-monday-morning-punchlines-709645dc, $5, entries close
26 Nov 2026 22:40 WIB, at most 200 characters).

How the winner was chosen (staging scorecard, 26 Nov 2026):
- Rubric (/10 per dimension, total = 0.4*theme + 0.3*originality
  + 0.15*density + 0.15*format) over 10 candidates. Rubric ranking:
  #4 9.2 > #8 8.9 > #1 8.7 > #6 8.6 > #5 8.5.
- Model-combo panel (gemini-4-hydrogen, one call, status 200): top-3
  #8 9.0, #6 8.5, #5 8.0; panel winner #8.
- Decision: combined score = average of rubric and panel. Winner #8:
  (8.9 + 9.0) / 2 = 8.95 — rubric #2 + panel #1, while rubric leader #4
  did not place in the panel top-3. The "five more minutes" premise is
  the most universal, and the escalation to "career decision" is sharper
  than #4's more niche custody metaphor.

Scoring honesty note: the panel published only its top-3, so #4 and #1
have no panel score on record and none is invented here. Their SCORES
entries below are UPPER BOUNDS — (rubric + 8.0) / 2, using the panel's
lowest published score (8.0) as the ceiling, since a finalist outside
the top-3 necessarily scored below it. The bound is conservative: even
at the bound, #4 (8.60) and #1 (8.35) stay below the winner's exact
combined score (8.95), so the pick does not depend on any invented
number.

The program re-derives the pick from the scores: highest combined score
wins, ties go to the earliest candidate in the list.
"""

import os

WINNER = "Monday morning: where 'just five more minutes' becomes a career decision."
MAX_CHARS = 200
ONE_WORD = False

# Top 5 of 10 candidates by combined score, highest first.
FINALISTS = [
    "Monday morning: where 'just five more minutes' becomes a career decision.",
    "My bed filed for custody of me on Monday mornings.",
    "I showed up to Monday like a software update nobody asked for.",
    "My alarm didn't wake me up; it just filed a complaint with HR.",
    "Monday is just Sunday's evil twin with a calendar invite.",
]

# Rubric totals (/10) from candidates.md, exactly as staged.
RUBRIC = {
    "Monday morning: where 'just five more minutes' becomes a career decision.": 8.9,
    "My bed filed for custody of me on Monday mornings.": 9.2,
    "My alarm didn't wake me up; it just filed a complaint with HR.": 8.7,
    "I showed up to Monday like a software update nobody asked for.": 8.6,
    "Monday is just Sunday's evil twin with a calendar invite.": 8.5,
}

# Gemini panel scores (/10) from the scorecard; only the top-3 were
# published. #4 and #1 have no panel score — see the docstring note.
PANEL = {
    "Monday morning: where 'just five more minutes' becomes a career decision.": 9.0,
    "I showed up to Monday like a software update nobody asked for.": 8.5,
    "Monday is just Sunday's evil twin with a calendar invite.": 8.0,
}

# Final combined score (/10) = (rubric + panel) / 2 where the panel
# score is published; otherwise an UPPER BOUND (rubric + 8.0) / 2 with
# 8.0 = the lowest published panel score. Winner's 8.95 is exact.
SCORES = {
    "Monday morning: where 'just five more minutes' becomes a career decision.": 8.95,
    "My bed filed for custody of me on Monday mornings.": 8.60,
    "I showed up to Monday like a software update nobody asked for.": 8.55,
    "My alarm didn't wake me up; it just filed a complaint with HR.": 8.35,
    "Monday is just Sunday's evil twin with a calendar invite.": 8.25,
}


def score(text: str) -> float:
    """Final combined score (/10) for a candidate."""
    return float(SCORES[text])


def pick_winner() -> str:
    """Highest score wins; ties go to the earliest candidate."""
    best = FINALISTS[0]
    best_score = score(best)
    for candidate in FINALISTS[1:]:
        candidate_score = score(candidate)
        if candidate_score > best_score:
            best, best_score = candidate, candidate_score
    return best


def validate(text: str) -> None:
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must contain non-whitespace text")
    if ONE_WORD and len(text.split()) != 1:
        raise ValueError("entry must be exactly one word")


def main() -> None:
    winner = pick_winner()
    validate(winner)

    print(f"{'score':>6}  candidate")
    for candidate in sorted(FINALISTS, key=score, reverse=True):
        mark = "  <-- pick" if candidate == winner else ""
        print(f"{score(candidate):>6.2f}  {candidate}{mark}")

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
