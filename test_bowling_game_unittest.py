import unittest
from bowling_game import BowlingGame


class TestBowlingGame(unittest.TestCase):
    """Test suite for BowlingGame (15 core cases per the Test Plan)."""

    def setUp(self):
        """Runs before every test method - gives each test a fresh game."""
        self.game = BowlingGame()

    def tearDown(self):
        """Runs after every test method."""
        pass

    def roll_many(self, rolls):
        for pins in rolls:
            self.game.roll(pins)

    # TC-01: Gutter game -- every ball scores zero
    def test_gutter_game(self):
        self.roll_many([0] * 20)
        self.assertEqual(self.game.score(), 0)

    # TC-02: Every ball knocks down 1 pin
    def test_all_ones(self):
        self.roll_many([1] * 20)
        self.assertEqual(self.game.score(), 20)

    # TC-03: Single open frame (3 + 6)
    def test_single_open_frame(self):
        self.roll_many([3, 6] + [0] * 18)
        self.assertEqual(self.game.score(), 9)

    # TC-04: Open frame worked example from spec (9 + miss)
    def test_open_frame_worked_example(self):
        self.roll_many([9, 0] + [0] * 18)
        self.assertEqual(self.game.score(), 9)

    # TC-05: Spare bonus -- next ball counted twice
    def test_spare_bonus(self):
        self.roll_many([5, 5, 5, 0] + [0] * 16)
        self.assertEqual(self.game.score(), 20)

    # TC-06: Spare in the 10th frame gets exactly 1 bonus ball
    def test_spare_in_tenth_frame(self):
        self.roll_many([0] * 18 + [5, 5, 7])
        self.assertEqual(self.game.score(), 17)

    # TC-07: All frames are spares (10 spares + 1 bonus ball)
    def test_all_spares(self):
        self.roll_many([5, 5] * 10 + [5])
        self.assertEqual(self.game.score(), 150)

    # TC-08: Strike worked example from spec
    def test_strike_worked_example(self):
        self.roll_many([10, 3, 6] + [0] * 16)
        self.assertEqual(self.game.score(), 28)

    # TC-09: Two consecutive strikes worked example from spec
    def test_two_consecutive_strikes(self):
        self.roll_many([10, 10, 4, 2] + [0] * 14)
        self.assertEqual(self.game.score(), 46)

    # TC-10: Perfect game -- 12 strikes
    def test_perfect_game(self):
        self.roll_many([10] * 12)
        self.assertEqual(self.game.score(), 300)

    # TC-11: Strike in the 10th frame gets exactly 2 bonus balls
    def test_strike_in_tenth_frame(self):
        self.roll_many([0] * 18 + [10, 3, 2])
        self.assertEqual(self.game.score(), 15)

    # TC-12: Maximum single-frame score (30) from 3 strikes in a row
    def test_three_strikes_in_a_row_frame_contribution(self):
        self.roll_many([10, 10, 10] + [0] * 14)
        self.assertEqual(10 + self.game._strike_bonus(0), 30)

    # TC-13: Reject negative pin counts
    def test_reject_negative_pins(self):
        with self.assertRaises(ValueError):
            self.game.roll(-1)

    # TC-14: Reject pin counts greater than 10
    def test_reject_pins_greater_than_ten(self):
        with self.assertRaises(ValueError):
            self.game.roll(11)

    # TC-15: Reject non-integer pin counts
    def test_reject_non_integer_pins(self):
        with self.assertRaises(TypeError):
            self.game.roll("5")


if __name__ == "__main__":
    unittest.main()
