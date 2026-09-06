import pytest
from bowling_game import BowlingGame


# Fixture: reusable setup component - gives each test a fresh game
@pytest.fixture
def game():
    return BowlingGame()


def roll_many(game, rolls):
    for pins in rolls:
        game.roll(pins)


# Parametrization: same scoring checks across many rolls/expected-score pairs
@pytest.mark.parametrize("rolls, expected_score", [
    ([0] * 20, 0),                    # TC-01 gutter game
    ([1] * 20, 20),                   # TC-02 all ones
    ([9, 0] + [0] * 18, 9),           # TC-04 open frame worked example
    ([5, 5, 5, 0] + [0] * 16, 20),    # TC-05 spare bonus
    ([10, 3, 6] + [0] * 16, 28),      # TC-08 strike worked example
    ([10, 10, 4, 2] + [0] * 14, 46),  # TC-09 two consecutive strikes
    ([10] * 12, 300),                 # TC-10 perfect game
])
def test_score_matrix(game, rolls, expected_score):
    roll_many(game, rolls)
    assert game.score() == expected_score


# Parametrization: input-validation checks across invalid pin counts
@pytest.mark.parametrize("bad_pins, expected_exception", [
    (-1, ValueError),     # TC-13 reject negative pin counts
    (11, ValueError),     # TC-14 reject pin counts greater than 10
    ("5", TypeError),     # TC-15 reject non-integer pin counts
])
def test_invalid_rolls_matrix(game, bad_pins, expected_exception):
    with pytest.raises(expected_exception):
        game.roll(bad_pins)
