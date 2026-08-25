"""
Main Entry Point - Number Guessing Game
Task-02: Create a Guessing Game (PRODIGY_SD_02)
"""

import sys
import argparse
from game_engine import GuessingGame, GuessResult


def run_cli_interactive():
    print("=" * 60)
    print("🎯  NUMBER GUESSING GAME (PRODIGY_SD_02)")
    print("=" * 60)
    print("Select Difficulty Level:")
    print("  1. Easy   (1 - 50)")
    print("  2. Medium (1 - 100)")
    print("  3. Hard   (1 - 500)")

    diff_choice = input("👉 Enter choice (1/2/3, default: 2): ").strip()
    if diff_choice == "1":
        min_v, max_v = 1, 50
    elif diff_choice == "3":
        min_v, max_v = 1, 500
    else:
        min_v, max_v = 1, 100

    game = GuessingGame(min_v, max_v)
    print(f"\n✨ I have chosen a random number between {min_v} and {max_v}!")
    print("Type your guess, or 'q' to quit.\n")

    while not game.is_game_over:
        try:
            user_input = input(f"[{game.current_lower_bound} - {game.current_upper_bound}] Enter your guess (Attempt #{game.attempts + 1}): ").strip()

            if user_input.lower() in ('q', 'quit', 'exit'):
                print(f"👋 Game ended. The secret number was: {game.secret_number}")
                break

            guess = int(user_input)
            result, msg = game.make_guess(guess)

            if result == GuessResult.TOO_LOW:
                print(f"   ⬆️  {msg}\n")
            elif result == GuessResult.TOO_HIGH:
                print(f"   ⬇️  {msg}\n")
            elif result == GuessResult.CORRECT:
                print("\n" + "=" * 50)
                print(f"🏆 {msg}")
                print("=" * 50 + "\n")
            else:
                print(f"   ⚠️  {msg}\n")

        except ValueError:
            print("   ❌ Invalid input! Please enter a valid integer.\n")
        except KeyboardInterrupt:
            print("\n👋 Game aborted.")
            break


def main():
    parser = argparse.ArgumentParser(description="Number Guessing Game (PRODIGY_SD_02)")
    parser.add_argument("--cli", action="store_true", help="Run the game in interactive terminal mode")

    args = parser.parse_args()

    if args.cli:
        run_cli_interactive()
        return

    try:
        from app_gui import launch_gui
        launch_gui()
    except Exception as e:
        print(f"ℹ️ Graphical mode unavailable or error ({e}). Launching terminal mode...")
        run_cli_interactive()


if __name__ == "__main__":
    main()
