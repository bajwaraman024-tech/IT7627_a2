# Bowling Game Scoring Engine — Testing & Maintenance

**IT7627 Software Testing and Maintenance — Project Assignment 2**
Student: Ramandeep Kaur (20250941)

## Overview

This repository contains the back-end scoring engine for a 10-pin bowling
educational game prototype, along with the full white-box unit testing,
debugging, and refactoring work carried out against it. No GUI or
data-access layer exists yet — this project covers the `BowlingGame` class
only, via `roll()` and `score()`.

## Project structure

```
.
├── bowling_game.py                  # current working version (see history below)
├── bowling_game_1_BASELINE_buggy.py # tutor-supplied original (unmodified)
├── bowling_game_2_FIXED_bugs_only.py# scoring bugs fixed, no validation yet
├── bowling_game_3_FINAL_refactored.py # final refactored version
├── test_bowling_game_unittest.py    # 15 core test cases (unittest)
├── test_bowling_game_pytest.py      # same rules, fixtures + parametrize (pytest)
├── bowling_game.html                # pydoc-generated API documentation
└── htmlcov/                         # coverage.py HTML report
```

## Approach

A 15-case test suite was written first, covering every business rule in
the brief: open frames, spares, strikes, consecutive strikes, the perfect
game, the 10th frame's bonus balls, and basic input validation. Running
this suite against the original tutor-supplied code before any changes
gave an objective, repeatable baseline of what was and wasn't working.

Three complementary frameworks are used:
- **doctest** — executable examples in `bowling_game.py`'s docstrings
- **unittest** — `test_bowling_game_unittest.py`, with `setUp()`/`tearDown()`
- **pytest** — `test_bowling_game_pytest.py`, using `@pytest.fixture` and
  `@pytest.mark.parametrize`

## Bugs found

| # | Bug | Symptom |
|---|-----|---------|
| 1 | `score()` looped `for frame in range(9)` instead of 10 frames | The entire 10th frame — including any strike/spare bonus — was never added to the score (a perfect game scored 270 instead of 300) |
| 2 | The open-frame branch added only `self.rolls[frame_index]`, dropping the second ball of the frame | Any open frame under-scored by exactly the value of its second ball (rolling 3 then 6 scored 3 instead of 9) |

11 of 15 unit tests failed against the original code, confirming both defects.

## Fixes and refactoring

- Fixed the loop bound (`range(9)` → `range(NUMBER_OF_FRAMES)`) and the
  open-frame calculation (sum both rolls, not just the first)
- Added validation to `roll()`: raises `ValueError` for pin counts outside
  0–10 and `TypeError` for non-integer input
- Replaced magic numbers with named constants `MAX_PINS` and
  `NUMBER_OF_FRAMES`
- Extracted the open-frame calculation into a `_frame_score()` helper,
  consistent with `_strike_bonus()`/`_spare_bonus()`
- Removed the unused `self.current_roll` attribute (dead state, written
  to but never read)

All 15 unit tests pass after refactoring, with no behavioural regressions.

## Running the tests

```bash
# unittest
python -m unittest test_bowling_game_unittest -v

# pytest
pytest test_bowling_game_pytest.py -v

# doctest
python -m doctest bowling_game.py -v
```

## Test coverage

```bash
coverage run -m unittest test_bowling_game_unittest -v
coverage report -m
coverage html   # then open htmlcov/index.html
```

## Documentation

API documentation (including the doctest examples) is generated with:

```bash
python -m pydoc -w bowling_game
```

## Recommendations for future work

- Add a validation check that also rejects a non-strike frame whose two
  balls sum to more than 10
- Add an `is_game_complete()` method so callers can check a game is
  finished before calling `score()`, avoiding an `IndexError` on an
  in-progress game
- Continue running the full regression suite before every future commit
