# Week 5 – Before / after

## Measures

| Measure | Before (`legacy_fees.py`) | After (`fees.py`) |
|---------|---------------------------|-------------------|
| Ruff issues (total) | 17 (16 with the handout's Ruff version) | **0** – `All checks passed!` |
| Highest cyclomatic complexity | 9 (`calc`) | **5** (`tuition_fee`) |
| Arguments of the main function | 6 | **5** (`courses, student_type, summer, discount, extras`) |
| Pylint score (/10) | 4.86 | **10.00** |
| Tests passing | 0 (no tests) | **16 passed** (10 in `test_grades.py`, 6 in `test_fees.py`) |

## Commit history of the refactoring (one commit per step)

1. Delete unused imports, `tmp` and argument `y`
2. Rename `calc`/`d`/`s`/`ProcessAll` to meaningful names
3. Constants and a `StudentType` enum
4. Rate table, `if summer:`, default discount `0`
5. `extras=()` and a `Course` dataclass
6. `report` returns text instead of printing
7. Fix the hidden bug (scholarship students get a fee)
8. Add docstrings (Pylint 10/10)

Notes:
- `test_fees.py` was committed first, before `fees.py` existed, so it was red (import error).
  It only becomes importable once `Course` and `StudentType` exist (steps 3 and 5). After step 5
  all tests passed except `test_scholarship_student_is_not_skipped`, which passed after step 7 as the handout expects.
  For steps 1–4 I checked behaviour against the legacy `calc` with a temporary comparison script.
- `legacy_fees.py` was left unchanged (and excluded from `ruff check .` / `ruff format .` in `pyproject.toml`),
  so that the characterization test can still compare old and new behaviour.

## Pairing reflection (3–4 sentences)

> **TODO – write this yourselves before submitting.** Each partner should add one or two sentences about
> your own experience: what was easier or harder as driver vs navigator, one bug or smell the other person
> spotted that you missed, and whether switching roles every 12 minutes helped.
