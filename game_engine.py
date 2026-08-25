"""
Core Game Engine - Number Guessing Game
Task-02: Create a Guessing Game (PRODIGY_SD_02)
"""

import random
from typing import Tuple, List, Optional
from enum import Enum


class GuessResult(Enum):
    TOO_LOW = "TOO_LOW"
    TOO_HIGH = "TOO_HIGH"
    CORRECT = "CORRECT"
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"
    ALREADY_GUESSED = "ALREADY_GUESSED"


class GuessingGame:
    """
    Manages the state and rules for the Number Guessing Game.
    """

    def __init__(self, min_val: int = 1, max_val: int = 100):
        self.min_val = min_val
        self.max_val = max_val
        self.secret_number = 0
        self.attempts = 0
        self.is_game_over = False
        self.guess_history: List[int] = []
        self.current_lower_bound = min_val
        self.current_upper_bound = max_val
        self.start_new_game()

    def start_new_game(self, min_val: Optional[int] = None, max_val: Optional[int] = None):
        """Starts a fresh game round with optional new range bounds."""
        if min_val is not None:
            self.min_val = min_val
        if max_val is not None:
            self.max_val = max_val

        self.secret_number = random.randint(self.min_val, self.max_val)
        self.attempts = 0
        self.is_game_over = False
        self.guess_history = []
        self.current_lower_bound = self.min_val
        self.current_upper_bound = self.max_val

    def make_guess(self, guess: int) -> Tuple[GuessResult, str]:
        """
        Evaluates a user's guess and returns the result and feedback message.
        """
        if self.is_game_over:
            return GuessResult.CORRECT, f"Game is already over! You won in {self.attempts} attempts."

        if guess < self.min_val or guess > self.max_val:
            return (
                GuessResult.OUT_OF_BOUNDS,
                f"Your guess {guess} is out of range! Please guess between {self.min_val} and {self.max_val}."
            )

        if guess in self.guess_history:
            return (
                GuessResult.ALREADY_GUESSED,
                f"You already guessed {guess}! Try a different number."
            )

        self.attempts += 1
        self.guess_history.append(guess)

        if guess < self.secret_number:
            if guess > self.current_lower_bound:
                self.current_lower_bound = guess + 1
            return (
                GuessResult.TOO_LOW,
                f"Too low! Try a higher number."
            )

        elif guess > self.secret_number:
            if guess < self.current_upper_bound:
                self.current_upper_bound = guess - 1
            return (
                GuessResult.TOO_HIGH,
                f"Too high! Try a lower number."
            )

        else:
            self.is_game_over = True
            return (
                GuessResult.CORRECT,
                f"Congratulations! You found the secret number ({self.secret_number}) in {self.attempts} attempts!"
            )
