"""
Bowling Game Implementation
A module for calculating bowling game scores.
"""
class BowlingGame:
    def __init__(self):
        # Initialize a new game with 10 frames
        # Each frame has up to 2 rolls (except the 10th frame which can have 3)
        self.rolls = []
        self.current_roll = 0

    def roll(self, pins):
        self.rolls.append(pins)
        self.current_roll += 1

    def score(self):
        score = 0
        frame_index = 0
        # BUG FIX 1: loop must cover all 10 frames, not 9 -
        # the original 'range(9)' silently dropped the whole 10th frame.
        for frame in range(10):
            if self._is_strike(frame_index):
                # Strike
                score += 10 + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                # Spare
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                # BUG FIX 2: an open frame must count BOTH balls, not just
                # the first one.
                score += self.rolls[frame_index] + self.rolls[frame_index + 1]
                frame_index += 2
        return score

    def _is_strike(self, frame_index):
        return frame_index < len(self.rolls) and self.rolls[frame_index] == 10

    def _is_spare(self, frame_index):
        return (
            frame_index + 1 < len(self.rolls)
            and self.rolls[frame_index] + self.rolls[frame_index + 1] == 10
        )

    def _strike_bonus(self, frame_index):
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

    def _spare_bonus(self, frame_index):
        return self.rolls[frame_index + 2]
