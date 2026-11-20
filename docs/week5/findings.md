# Week 5 – Findings on `legacy_fees.py`

Tools: Ruff 0.17.6, Pylint 4.1.4. Full terminal output is in `before.txt`.

**Before-scores:** Ruff reports **17** problems (the handout says 16; this newer Ruff
also reports `PLR0917 too-many-positional-arguments`, which sits next to `PLR0913`).
Pylint score: **4.86 / 10**.

## C1. Findings table

| Rule | Count | Smell (lecture name) | Refactoring |
|------|-------|----------------------|-------------|
| F401 | 2 | Dead code (unused imports) | Delete the imports |
| PLR2004 | 6 | Magic numbers | Replace with named constants / an enum |
| C901 | 1 | Long method / complex conditional logic (`calc` has complexity 9, limit 5) | Replace the if/elif chain with a rate table (lookup instead of branching); extract small functions |
| PLR0913 (+ PLR0917) | 1 (+1) | Long parameter list | Remove unused parameters, group related data into objects (e.g. a `Course` class), give optional values defaults |
| ARG001 | 1 | Dead code (unused parameter `y`) | Remove the parameter and update every caller |
| B006 | 1 | Mutable default argument (a bug waiting to happen: shared state between calls) | Use an immutable default, e.g. `extras=()` (or `None`) |
| E711 / E712 | 1 / 1 | Poor condition style (`== None`, `== True`) | Use `if summer:` and a default of `0` for the discount (or `is not None`) |
| F841 | 1 | Dead code (unused variable `tmp`) | Delete the variable |
| N802 | 1 | Bad naming (`ProcessAll` breaks the naming convention) | Rename to `process_all` (Rename Function) |

Pylint's own names for the same problems: `unused-import`, `unused-argument`,
`unused-variable`, `dangerous-default-value`, `singleton-comparison`, `invalid-name`,
`too-many-arguments`. It also reports `missing-function-docstring` /
`missing-module-docstring` and `possibly-used-before-assignment` (line 41, `fee`),
which hints at the hidden bug below.

## C2. Smells the tools did not report

1. **Mysterious names** – `d`, `t`, `s`, `y`, `c`, `x`, `st`, `e`, `disc`. Nobody can tell what `t` is without
   reading the comment above it.
2. **Primitive obsession / type codes** – the student kind is a bare `1/2/3`, and a course is a
   dictionary with a cryptic key `"h"`. A typo in either is silent.
3. **Mixed responsibilities** – `report` both calculates (through `calc`) and prints, and `ProcessAll` prints
   instead of returning data, so none of it can be tested without capturing console output.
4. **Duplicated code** – `ProcessAll` has two near-identical `calc(...)` calls, and the thresholds
   (`6000`, the type codes) are repeated in `calc` and `report`.
5. **Comment as deodorant** – `# t: 1=student, 2=staff child, 3=scholarship` explains a bad design
   instead of fixing it (an `Enum` makes the comment unnecessary).
6. **Pointless code** – `total = total + 0`, `tmp = total * 1.0`, and the hard-coded `2026` passed to a
   parameter that is never used.
7. **No tests and no docstrings** – there is no safety net for changing anything.

## Hidden bug in `ProcessAll`

`ProcessAll` only assigns `fee` inside `if st["type"] == 1` and `if st["type"] == 2`. For a scholarship
student (type 3) neither `if` runs, so `fee` is **not updated** and `print(st["name"], fee)` prints the
fee left over from the previous student – so Omar is shown paying 1050 instead of 0. If Omar were the
*first* student, `fee` would never have been assigned and the function would crash with
`UnboundLocalError` (I reproduced this). Pylint's `possibly-used-before-assignment` warning pointed at this line.
The fix (step 7) calculates a fee for every student via the `StudentType` enum and a rate table, where
scholarship students have a factor of 0.
