"""
Bowling Game Implementation
A module for calculating bowling game scores.

This module implements the scoring engine for a standard ten-pin
bowling game, including open frames, spares, strikes, and the
special two/three-ball bonus rules for the tenth frame.
"""

MAX_PINS = 10
NUMBER_OF_FRAMES = 10


class BowlingGame:
    """Records rolls for a single game and calculates the final score.

    Examples:
        >>> game = BowlingGame()
        >>> for _ in range(20):
        ...     game.roll(0)
        >>> game.score()
        0
    """

    def __init__(self):
        """Initialize a new game with no rolls recorded yet."""
        self.rolls = []

    def roll(self, pins):
        """Record the number of pins knocked down by one roll.

        Args:
            pins (int): Number of pins knocked down, 0-10 inclusive.

        Raises:
            TypeError: If pins is not an integer.
            ValueError: If pins is outside the 0-10 range.

        Examples:
            >>> game = BowlingGame()
            >>> game.roll(5)
            >>> game.roll(11)
            Traceback (most recent call last):
                ...
            ValueError: pins must be between 0 and 10.
            >>> game.roll(-1)
            Traceback (most recent call last):
                ...
            ValueError: pins must be between 0 and 10.
            >>> game.roll("five")
            Traceback (most recent call last):
                ...
            TypeError: pins must be an integer.
        """
        if isinstance(pins, bool) or not isinstance(pins, int):
            raise TypeError("pins must be an integer.")
        if pins < 0 or pins > MAX_PINS:
            raise ValueError("pins must be between 0 and 10.")
        self.rolls.append(pins)

    def score(self):
        """Calculate the total score for a completed game.

        Returns:
            int: The final score, 0-300.

        Examples:
            >>> game = BowlingGame()
            >>> for _ in range(12):
            ...     game.roll(10)
            >>> game.score()
            300
        """
        score = 0
        frame_index = 0
        for _ in range(NUMBER_OF_FRAMES):
            if self._is_strike(frame_index):
                score += MAX_PINS + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                score += MAX_PINS + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                score += self._frame_score(frame_index)
                frame_index += 2
        return score

    def _is_strike(self, frame_index):
        """Return True if the roll at frame_index is a strike."""
        return frame_index < len(self.rolls) and self.rolls[frame_index] == MAX_PINS

    def _is_spare(self, frame_index):
        """Return True if the two rolls starting at frame_index form a spare."""
        return (
            frame_index + 1 < len(self.rolls)
            and self.rolls[frame_index] + self.rolls[frame_index + 1] == MAX_PINS
        )

    def _strike_bonus(self, frame_index):
        """Return the bonus (next two rolls) awarded for a strike."""
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

    def _spare_bonus(self, frame_index):
        """Return the bonus (next one roll) awarded for a spare."""
        return self.rolls[frame_index + 2]

    def _frame_score(self, frame_index):
        """Return the total pins knocked down in an open frame."""
        return self.rolls[frame_index] + self.rolls[frame_index + 1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
