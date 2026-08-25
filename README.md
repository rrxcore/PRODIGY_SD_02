# Number Guessing Game

An interactive desktop application and terminal game where the player attempts to guess a randomly generated number with dynamic feedback and attempt tracking.

---

## Features

- **Dynamic Feedback:** Instant hints indicating whether your guess is "Too High", "Too Low", or "Correct!".
- **Attempt Tracking:** Keeps count of total guesses taken to find the target.
- **Adaptive Range Bounds:** Real-time visual indicator of the remaining valid range based on previous guesses.
- **Difficulty Modes:** Easy (1–50), Medium (1–100), and Hard (1–500).
- **Desktop GUI:** Modern dark-themed user interface built using `tkinter`.
- **CLI Mode:** Full command-line interactive support.
- **Unit Tested:** Built-in test suite using Python's `unittest`.

---

## Installation & Usage

### Prerequisites
- Python 3.8+ (No third-party packages required)

### Run Desktop GUI
```bash
python main.py
```

### Run Terminal / CLI Mode
```bash
python main.py --cli
```

---

## Project Structure

```
PRODIGY_SD_02/
├── game_engine.py       # Core game logic, state, and comparison rules
├── app_gui.py           # Desktop graphical interface
├── main.py              # Application entry point (GUI & CLI)
├── test_game.py         # Automated unit tests
├── requirements.txt     # Dependency information
├── .gitignore
└── README.md
```

---

## Running Tests

```bash
python -m unittest test_game.py -v
```

---

## License
MIT License
