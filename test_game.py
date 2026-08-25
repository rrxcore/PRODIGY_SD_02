"""
Automated Unit Tests for Number Guessing Game
Task-02: Create a Guessing Game (PRODIGY_SD_02)
"""

import unittest
from game_engine import GuessingGame, GuessResult


class TestGuessingGame(unittest.TestCase):

    def setUp(self):
        self.game = GuessingGame(1, 100)
        # Fix secret number for deterministic testing
        self.game.secret_number = 42

    def test_initial_state(self):
        self.assertEqual(self.game.min_val, 1)
        self.assertEqual(self.game.max_val, 100)
        self.assertEqual(self.game.attempts, 0)
        self.assertFalse(self.game.is_game_over)
        self.assertEqual(self.game.guess_history, [])

    def test_too_low_guess(self):
        res, msg = self.game.make_guess(20)
        self.assertEqual(res, GuessResult.TOO_LOW)
        self.assertEqual(self.game.attempts, 1)
        self.assertEqual(self.game.current_lower_bound, 21)
        self.assertFalse(self.game.is_game_over)

    def test_too_high_guess(self):
        res, msg = self.game.make_guess(80)
        self.assertEqual(res, GuessResult.TOO_HIGH)
        self.assertEqual(self.game.attempts, 1)
        self.assertEqual(self.game.current_upper_bound, 79)
        self.assertFalse(self.game.is_game_over)

    def test_correct_guess(self):
        res, msg = self.game.make_guess(42)
        self.assertEqual(res, GuessResult.CORRECT)
        self.assertEqual(self.game.attempts, 1)
        self.assertTrue(self.game.is_game_over)
        self.assertIn("1 attempts", msg)

    def test_attempt_counter_progression(self):
        self.game.make_guess(10) # Too low (att 1)
        self.game.make_guess(90) # Too high (att 2)
        self.game.make_guess(30) # Too low (att 3)
        res, msg = self.game.make_guess(42) # Correct (att 4)

        self.assertEqual(self.game.attempts, 4)
        self.assertTrue(self.game.is_game_over)
        self.assertEqual(res, GuessResult.CORRECT)

    def test_out_of_bounds_guess(self):
        res, _ = self.game.make_guess(-5)
        self.assertEqual(res, GuessResult.OUT_OF_BOUNDS)
        self.assertEqual(self.game.attempts, 0) # Out of bounds doesn't waste attempt

        res, _ = self.game.make_guess(150)
        self.assertEqual(res, GuessResult.OUT_OF_BOUNDS)
        self.assertEqual(self.game.attempts, 0)

    def test_already_guessed(self):
        self.game.make_guess(25)
        self.assertEqual(self.game.attempts, 1)

        res, msg = self.game.make_guess(25)
        self.assertEqual(res, GuessResult.ALREADY_GUESSED)
        self.assertEqual(self.game.attempts, 1) # Doesn't double count

    def test_start_new_game_reset(self):
        self.game.make_guess(10)
        self.game.make_guess(42)
        self.assertTrue(self.game.is_game_over)

        self.game.start_new_game(1, 50)
        self.assertEqual(self.game.min_val, 1)
        self.assertEqual(self.game.max_val, 50)
        self.assertEqual(self.game.attempts, 0)
        self.assertFalse(self.game.is_game_over)
        self.assertEqual(self.game.guess_history, [])


if __name__ == "__main__":
    unittest.main()
