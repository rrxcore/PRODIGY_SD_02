"""
Modern Desktop GUI for Number Guessing Game
Task-02: Create a Guessing Game (PRODIGY_SD_02)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from game_engine import GuessingGame, GuessResult


class GuessingGameGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("780x640")
        self.root.minsize(720, 580)

        # Color Theme - Dark Slate Modern
        self.BG_MAIN = "#0f172a"
        self.BG_CARD = "#1e293b"
        self.BG_INPUT = "#334155"
        self.TEXT_PRIMARY = "#f8fafc"
        self.TEXT_MUTED = "#94a3b8"
        self.ACCENT_CYAN = "#38bdf8"
        self.ACCENT_EMERALD = "#10b981"
        self.ACCENT_AMBER = "#f59e0b"
        self.ACCENT_ROSE = "#f43f5e"
        self.BORDER_COLOR = "#475569"

        self.root.configure(bg=self.BG_MAIN)
        self.setup_styles()

        # State
        self.game = GuessingGame(1, 100)
        self.difficulty_var = tk.StringVar(value="Medium (1-100)")
        self.guess_input_var = tk.StringVar()

        self.build_ui()
        self.update_stats()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Custom.TCombobox",
            fieldbackground=self.BG_INPUT,
            background=self.BG_CARD,
            foreground=self.TEXT_PRIMARY,
            arrowcolor=self.ACCENT_CYAN,
            bordercolor=self.BORDER_COLOR,
            darkcolor=self.BG_CARD,
            lightcolor=self.BG_CARD
        )
        style.map(
            "Custom.TCombobox",
            fieldbackground=[("readonly", self.BG_INPUT)],
            foreground=[("readonly", self.TEXT_PRIMARY)]
        )

    def build_ui(self):
        # Header Container
        header_frame = tk.Frame(self.root, bg=self.BG_MAIN, pady=15, padx=25)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_frame,
            text="🎯 Number Guessing Game",
            font=("Segoe UI", 20, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_MAIN
        )
        title_lbl.pack(anchor="w")

        # Main Content Frame
        content_frame = tk.Frame(self.root, bg=self.BG_MAIN, padx=25)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # ---------------- Top Settings Card (Difficulty & Reset) ----------------
        top_card = tk.Frame(
            content_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=18,
            pady=12
        )
        top_card.pack(fill=tk.X, pady=(0, 15))

        diff_lbl = tk.Label(
            top_card,
            text="Difficulty:",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_MUTED,
            bg=self.BG_CARD
        )
        diff_lbl.pack(side=tk.LEFT, padx=(0, 10))

        self.diff_combo = ttk.Combobox(
            top_card,
            textvariable=self.difficulty_var,
            values=["Easy (1-50)", "Medium (1-100)", "Hard (1-500)"],
            state="readonly",
            width=16,
            style="Custom.TCombobox",
            font=("Segoe UI", 10)
        )
        self.diff_combo.pack(side=tk.LEFT, padx=(0, 15), ipady=2)
        self.diff_combo.bind("<<ComboboxSelected>>", lambda e: self.on_difficulty_change())

        self.btn_new_game = tk.Button(
            top_card,
            text="🔄 New Game / Reset",
            font=("Segoe UI", 9, "bold"),
            bg=self.BG_INPUT,
            fg=self.ACCENT_CYAN,
            activebackground=self.ACCENT_CYAN,
            activeforeground=self.BG_MAIN,
            bd=0,
            cursor="hand2",
            command=self.reset_game,
            padx=12,
            pady=4
        )
        self.btn_new_game.pack(side=tk.RIGHT)

        # ---------------- Stats Row (Attempts & Range Bounds) ----------------
        stats_frame = tk.Frame(content_frame, bg=self.BG_MAIN)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        # Attempts Card
        self.card_attempts = tk.Frame(
            stats_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=15,
            pady=10
        )
        self.card_attempts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        att_title = tk.Label(
            self.card_attempts,
            text="ATTEMPTS",
            font=("Segoe UI", 9, "bold"),
            fg=self.TEXT_MUTED,
            bg=self.BG_CARD
        )
        att_title.pack(anchor="w")

        self.lbl_attempts_val = tk.Label(
            self.card_attempts,
            text="0",
            font=("Segoe UI", 20, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD
        )
        self.lbl_attempts_val.pack(anchor="w")

        # Range Card
        self.card_range = tk.Frame(
            stats_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=15,
            pady=10
        )
        self.card_range.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))

        range_title = tk.Label(
            self.card_range,
            text="POSSIBLE RANGE",
            font=("Segoe UI", 9, "bold"),
            fg=self.TEXT_MUTED,
            bg=self.BG_CARD
        )
        range_title.pack(anchor="w")

        self.lbl_range_val = tk.Label(
            self.card_range,
            text="1 - 100",
            font=("Segoe UI", 20, "bold"),
            fg=self.ACCENT_CYAN,
            bg=self.BG_CARD
        )
        self.lbl_range_val.pack(anchor="w")

        # ---------------- Input & Action Section ----------------
        action_card = tk.Frame(
            content_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=20,
            pady=15
        )
        action_card.pack(fill=tk.X, pady=(0, 15))

        prompt_lbl = tk.Label(
            action_card,
            text="Enter your guess:",
            font=("Segoe UI", 11, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD
        )
        prompt_lbl.grid(row=0, column=0, sticky="w", padx=(0, 12))

        self.entry_guess = tk.Entry(
            action_card,
            textvariable=self.guess_input_var,
            font=("Segoe UI", 14, "bold"),
            bg=self.BG_INPUT,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.TEXT_PRIMARY,
            bd=0,
            relief=tk.FLAT,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            width=12
        )
        self.entry_guess.grid(row=0, column=1, sticky="w", padx=(0, 15), ipady=4)
        self.entry_guess.bind("<Return>", lambda e: self.submit_guess())
        self.entry_guess.focus_set()

        self.btn_guess = tk.Button(
            action_card,
            text="Submit Guess 🚀",
            font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT_CYAN,
            fg=self.BG_MAIN,
            activebackground=self.ACCENT_EMERALD,
            activeforeground=self.TEXT_PRIMARY,
            bd=0,
            cursor="hand2",
            command=self.submit_guess,
            padx=18,
            pady=5
        )
        self.btn_guess.grid(row=0, column=2, sticky="w")

        # ---------------- Feedback Banner ----------------
        self.banner_frame = tk.Frame(
            content_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=15,
            pady=12
        )
        self.banner_frame.pack(fill=tk.X, pady=(0, 15))

        self.lbl_feedback = tk.Label(
            self.banner_frame,
            text="🤔 I have picked a random number. Make your first guess!",
            font=("Segoe UI", 12, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD,
            wraplength=680,
            justify=tk.LEFT
        )
        self.lbl_feedback.pack(anchor="w")

        # ---------------- Guess History Log ----------------
        hist_frame = tk.Frame(
            content_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=15,
            pady=10
        )
        hist_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        hist_title = tk.Label(
            hist_frame,
            text="📜 Guess History",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD
        )
        hist_title.pack(anchor="w", pady=(0, 5))

        self.txt_history = tk.Text(
            hist_frame,
            height=5,
            bg=self.BG_INPUT,
            fg=self.TEXT_PRIMARY,
            font=("Consolas", 10),
            bd=0,
            relief=tk.FLAT,
            padx=10,
            pady=8
        )
        self.txt_history.pack(fill=tk.BOTH, expand=True)

    def on_difficulty_change(self):
        choice = self.difficulty_var.get()
        if "500" in choice:
            self.game.start_new_game(1, 500)
        elif "50" in choice:
            self.game.start_new_game(1, 50)
        else:
            self.game.start_new_game(1, 100)
        self.reset_ui_state()

    def reset_game(self):
        self.on_difficulty_change()

    def reset_ui_state(self):
        self.guess_input_var.set("")
        self.entry_guess.config(state="normal")
        self.btn_guess.config(state="normal", text="Submit Guess 🚀", bg=self.ACCENT_CYAN)
        self.lbl_feedback.config(
            text=f"🤔 I have picked a random number between {self.game.min_val} and {self.game.max_val}. Guess it!",
            fg=self.TEXT_PRIMARY
        )
        self.banner_frame.config(bg=self.BG_CARD)
        self.lbl_feedback.config(bg=self.BG_CARD)
        self.txt_history.delete("1.0", tk.END)
        self.update_stats()
        self.entry_guess.focus_set()

    def update_stats(self):
        self.lbl_attempts_val.config(text=str(self.game.attempts))
        self.lbl_range_val.config(text=f"{self.game.current_lower_bound} - {self.game.current_upper_bound}")

    def submit_guess(self):
        raw_val = self.guess_input_var.get().strip()
        if not raw_val:
            return

        try:
            guess_val = int(raw_val)
        except ValueError:
            self.lbl_feedback.config(text="⚠️ Please enter a whole integer number!", fg=self.ACCENT_ROSE)
            return

        result, msg = self.game.make_guess(guess_val)
        self.guess_input_var.set("")
        self.update_stats()

        # Visual feedback colors
        if result == GuessResult.TOO_LOW:
            self.lbl_feedback.config(text=f"⬆️ {msg} (Guessed: {guess_val})", fg=self.ACCENT_AMBER)
            self.append_history(f"Attempt #{self.game.attempts}: {guess_val} -> Too Low ⬆️")

        elif result == GuessResult.TOO_HIGH:
            self.lbl_feedback.config(text=f"⬇️ {msg} (Guessed: {guess_val})", fg=self.ACCENT_ROSE)
            self.append_history(f"Attempt #{self.game.attempts}: {guess_val} -> Too High ⬇️")

        elif result == GuessResult.CORRECT:
            self.lbl_feedback.config(text=f"🎉 {msg}", fg=self.ACCENT_EMERALD)
            self.append_history(f"Attempt #{self.game.attempts}: {guess_val} -> WINNER! 🏆")
            self.entry_guess.config(state="disabled")
            self.btn_guess.config(state="disabled", text="Victory! 🏆", bg=self.ACCENT_EMERALD)

        elif result in (GuessResult.OUT_OF_BOUNDS, GuessResult.ALREADY_GUESSED):
            self.lbl_feedback.config(text=f"⚠️ {msg}", fg=self.ACCENT_AMBER)

    def append_history(self, text: str):
        self.txt_history.insert(tk.END, text + "\n")
        self.txt_history.see(tk.END)


def launch_gui():
    root = tk.Tk()
    app = GuessingGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
