"""
Modern Desktop GUI for Number Guessing Game
Task-02: Create a Guessing Game (PRODIGY_SD_02)
"""

import tkinter as tk
from tkinter import ttk
from game_engine import GuessingGame, GuessResult


class GuessingGameGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("820x690")
        self.root.minsize(760, 640)

        # Refined Modern Dark Theme Palette
        self.BG_MAIN = "#0a0e1a"        # Deepest midnight slate
        self.BG_CARD = "#131b2e"        # Elevated card surface
        self.BG_CARD_LIGHT = "#1a243b"  # Secondary surface
        self.BG_INPUT = "#1e293d"       # Input background
        self.TEXT_PRIMARY = "#f8fafc"   # High contrast crisp white
        self.TEXT_MUTED = "#94a3b8"     # Subdued secondary text
        self.ACCENT_CYAN = "#38bdf8"    # Electric Cyan
        self.ACCENT_INDIGO = "#6366f1"  # Indigo accent
        self.ACCENT_EMERALD = "#10b981" # Victory Emerald
        self.ACCENT_AMBER = "#f59e0b"   # Warm Amber (Too Low)
        self.ACCENT_ROSE = "#f43f5e"    # Vibrant Rose (Too High)
        self.BORDER_COLOR = "#222f46"   # Subtle clean border

        self.root.configure(bg=self.BG_MAIN)

        # Game State
        self.game = GuessingGame(1, 100)
        self.current_diff_mode = "medium"
        self.guess_input_var = tk.StringVar()
        self.best_score = None  # Minimum attempts achieved in session

        self.build_ui()
        self.update_stats()

    def build_ui(self):
        # ---------------- Header Container ----------------
        header_frame = tk.Frame(self.root, bg=self.BG_MAIN, pady=16, padx=28)
        header_frame.pack(fill=tk.X)

        header_top = tk.Frame(header_frame, bg=self.BG_MAIN)
        header_top.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_top,
            text="🎯 Number Guessing Game",
            font=("Segoe UI", 21, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_MAIN
        )
        title_lbl.pack(side=tk.LEFT)

        self.btn_reset = tk.Button(
            header_top,
            text="🔄 Restart Game",
            font=("Segoe UI", 9, "bold"),
            bg=self.BG_CARD,
            fg=self.ACCENT_CYAN,
            activebackground=self.ACCENT_CYAN,
            activeforeground=self.BG_MAIN,
            bd=1,
            relief=tk.SOLID,
            highlightbackground=self.BORDER_COLOR,
            cursor="hand2",
            command=self.reset_game,
            padx=14,
            pady=5
        )
        self.btn_reset.pack(side=tk.RIGHT)

        subtitle_lbl = tk.Label(
            header_frame,
            text="Can you crack the secret number in the fewest possible attempts?",
            font=("Segoe UI", 9),
            fg=self.TEXT_MUTED,
            bg=self.BG_MAIN
        )
        subtitle_lbl.pack(anchor="w", pady=(3, 0))

        # ---------------- Main Content Frame ----------------
        content_frame = tk.Frame(self.root, bg=self.BG_MAIN, padx=28)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # ---------------- Difficulty Selector Pill Bar ----------------
        diff_card = tk.Frame(
            content_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=16,
            pady=10
        )
        diff_card.pack(fill=tk.X, pady=(0, 14))

        diff_lbl = tk.Label(
            diff_card,
            text="Difficulty Mode:",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_MUTED,
            bg=self.BG_CARD
        )
        diff_lbl.pack(side=tk.LEFT, padx=(0, 15))

        self.diff_buttons = {}
        diff_options = [
            ("Easy (1-50)", "easy", 1, 50),
            ("Medium (1-100)", "medium", 1, 100),
            ("Hard (1-500)", "hard", 1, 500)
        ]

        for label, mode_key, min_v, max_v in diff_options:
            btn = tk.Button(
                diff_card,
                text=label,
                font=("Segoe UI", 9, "bold" if mode_key == "medium" else "normal"),
                bg=self.ACCENT_INDIGO if mode_key == "medium" else self.BG_INPUT,
                fg=self.TEXT_PRIMARY,
                activebackground=self.ACCENT_CYAN,
                activeforeground=self.BG_MAIN,
                bd=0,
                cursor="hand2",
                command=lambda m=mode_key, min_val=min_v, max_val=max_v: self.select_difficulty(m, min_val, max_val),
                padx=12,
                pady=4
            )
            btn.pack(side=tk.LEFT, padx=4)
            self.diff_buttons[mode_key] = btn

        # ---------------- Stats Overview Row (3 Cards) ----------------
        stats_frame = tk.Frame(content_frame, bg=self.BG_MAIN)
        stats_frame.pack(fill=tk.X, pady=(0, 14))

        # Card 1: Attempts
        self.card_att = self.create_stat_card(stats_frame, "ATTEMPTS", "0", self.TEXT_PRIMARY)
        self.card_att.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        # Card 2: Remaining Range
        self.card_rng = self.create_stat_card(stats_frame, "POSSIBLE RANGE", "1 - 100", self.ACCENT_CYAN)
        self.card_rng.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 6))

        # Card 3: Best Score
        self.card_best = self.create_stat_card(stats_frame, "BEST SCORE", "--", self.ACCENT_EMERALD)
        self.card_best.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))

        # ---------------- Dynamic Visual Feedback Banner ----------------
        self.banner_frame = tk.Frame(
            content_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=18,
            pady=14
        )
        self.banner_frame.pack(fill=tk.X, pady=(0, 14))

        self.lbl_feedback_icon = tk.Label(
            self.banner_frame,
            text="🤔",
            font=("Segoe UI", 18),
            bg=self.BG_CARD
        )
        self.lbl_feedback_icon.pack(side=tk.LEFT, padx=(0, 12))

        self.lbl_feedback = tk.Label(
            self.banner_frame,
            text="I've chosen a secret number! Make your first guess below.",
            font=("Segoe UI", 11, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD,
            wraplength=650,
            justify=tk.LEFT
        )
        self.lbl_feedback.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ---------------- Input Action Card ----------------
        input_card = tk.Frame(
            content_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=20,
            pady=16
        )
        input_card.pack(fill=tk.X, pady=(0, 14))

        prompt_lbl = tk.Label(
            input_card,
            text="Enter Your Guess:",
            font=("Segoe UI", 11, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD
        )
        prompt_lbl.grid(row=0, column=0, sticky="w", padx=(0, 14))

        self.entry_guess = tk.Entry(
            input_card,
            textvariable=self.guess_input_var,
            font=("Segoe UI", 14, "bold"),
            bg=self.BG_INPUT,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.TEXT_PRIMARY,
            bd=0,
            relief=tk.FLAT,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            width=14
        )
        self.entry_guess.grid(row=0, column=1, sticky="w", padx=(0, 15), ipady=5)
        self.entry_guess.bind("<Return>", lambda e: self.submit_guess())
        self.entry_guess.focus_set()

        self.btn_guess = tk.Button(
            input_card,
            text="Submit Guess 🚀",
            font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT_CYAN,
            fg=self.BG_MAIN,
            activebackground=self.ACCENT_EMERALD,
            activeforeground=self.TEXT_PRIMARY,
            bd=0,
            cursor="hand2",
            command=self.submit_guess,
            padx=20,
            pady=6
        )
        self.btn_guess.grid(row=0, column=2, sticky="w")

        # ---------------- Guess History Card ----------------
        hist_frame = tk.Frame(
            content_frame,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=18,
            pady=12
        )
        hist_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        hist_header = tk.Frame(hist_frame, bg=self.BG_CARD)
        hist_header.pack(fill=tk.X, pady=(0, 6))

        hist_title = tk.Label(
            hist_header,
            text="📜 Guess Activity Log",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD
        )
        hist_title.pack(side=tk.LEFT)

        btn_clear = tk.Button(
            hist_header,
            text="Clear Log",
            font=("Segoe UI", 8),
            bg=self.BG_INPUT,
            fg=self.TEXT_MUTED,
            activebackground=self.ACCENT_ROSE,
            activeforeground=self.TEXT_PRIMARY,
            bd=0,
            cursor="hand2",
            command=self.clear_history,
            padx=8,
            pady=2
        )
        btn_clear.pack(side=tk.RIGHT)

        self.txt_history = tk.Text(
            hist_frame,
            height=5,
            bg=self.BG_INPUT,
            fg=self.TEXT_PRIMARY,
            font=("Consolas", 10),
            bd=0,
            relief=tk.FLAT,
            padx=12,
            pady=8
        )
        self.txt_history.pack(fill=tk.BOTH, expand=True)

    def create_stat_card(self, parent: tk.Frame, title: str, init_val: str, accent_color: str):
        card = tk.Frame(
            parent,
            bg=self.BG_CARD,
            bd=1,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=14,
            pady=10
        )
        lbl_t = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            fg=self.TEXT_MUTED,
            bg=self.BG_CARD
        )
        lbl_t.pack(anchor="w")

        lbl_v = tk.Label(
            card,
            text=init_val,
            font=("Segoe UI", 18, "bold"),
            fg=accent_color,
            bg=self.BG_CARD
        )
        lbl_v.pack(anchor="w", pady=(2, 0))

        # Attach label reference to widget for easy updates
        card.lbl_value = lbl_v
        return card

    def select_difficulty(self, mode: str, min_val: int, max_val: int):
        self.current_diff_mode = mode
        for k, btn in self.diff_buttons.items():
            if k == mode:
                btn.config(bg=self.ACCENT_INDIGO, font=("Segoe UI", 9, "bold"))
            else:
                btn.config(bg=self.BG_INPUT, font=("Segoe UI", 9, "normal"))

        self.game.start_new_game(min_val, max_val)
        self.reset_ui_state()

    def reset_game(self):
        self.game.start_new_game()
        self.reset_ui_state()

    def reset_ui_state(self):
        self.guess_input_var.set("")
        self.entry_guess.config(state="normal")
        self.btn_guess.config(state="normal", text="Submit Guess 🚀", bg=self.ACCENT_CYAN, fg=self.BG_MAIN)
        self.set_feedback_state("default", "🤔", f"I've chosen a number between {self.game.min_val} and {self.game.max_val}. Guess it!")
        self.txt_history.delete("1.0", tk.END)
        self.update_stats()
        self.entry_guess.focus_set()

    def update_stats(self):
        self.card_att.lbl_value.config(text=str(self.game.attempts))
        self.card_rng.lbl_value.config(text=f"{self.game.current_lower_bound} - {self.game.current_upper_bound}")
        if self.best_score is not None:
            self.card_best.lbl_value.config(text=f"{self.best_score} tries")
        else:
            self.card_best.lbl_value.config(text="--")

    def set_feedback_state(self, state: str, icon: str, message: str):
        self.lbl_feedback_icon.config(text=icon)
        self.lbl_feedback.config(text=message)

        if state == "low":
            color = self.ACCENT_AMBER
            bg_box = "#23180c"
        elif state == "high":
            color = self.ACCENT_ROSE
            bg_box = "#230f16"
        elif state == "win":
            color = self.ACCENT_EMERALD
            bg_box = "#0d261c"
        else:
            color = self.TEXT_PRIMARY
            bg_box = self.BG_CARD

        self.banner_frame.config(bg=bg_box, highlightbackground=color if state != "default" else self.BORDER_COLOR)
        self.lbl_feedback_icon.config(bg=bg_box)
        self.lbl_feedback.config(bg=bg_box, fg=color)

    def submit_guess(self):
        raw_val = self.guess_input_var.get().strip()
        if not raw_val:
            return

        try:
            guess_val = int(raw_val)
        except ValueError:
            self.set_feedback_state("high", "⚠️", "Please enter a valid whole number!")
            return

        result, msg = self.game.make_guess(guess_val)
        self.guess_input_var.set("")
        self.update_stats()

        if result == GuessResult.TOO_LOW:
            self.set_feedback_state("low", "⬆️", f"Too Low! Aim higher than {guess_val}.")
            self.append_history(f"#{self.game.attempts:02d} | Guess: {guess_val:<4} ➔ TOO LOW  ⬆️  [Range: {self.game.current_lower_bound} - {self.game.current_upper_bound}]")

        elif result == GuessResult.TOO_HIGH:
            self.set_feedback_state("high", "⬇️", f"Too High! Aim lower than {guess_val}.")
            self.append_history(f"#{self.game.attempts:02d} | Guess: {guess_val:<4} ➔ TOO HIGH ⬇️  [Range: {self.game.current_lower_bound} - {self.game.current_upper_bound}]")

        elif result == GuessResult.CORRECT:
            self.set_feedback_state("win", "🏆", f"VICTORY! You guessed {guess_val} correctly in {self.game.attempts} attempts!")
            self.append_history(f"#{self.game.attempts:02d} | Guess: {guess_val:<4} ➔ WINNER! 🏆 (Completed in {self.game.attempts} attempts)")
            self.entry_guess.config(state="disabled")
            self.btn_guess.config(state="disabled", text="Victory! 🏆", bg=self.ACCENT_EMERALD, fg=self.TEXT_PRIMARY)

            if self.best_score is None or self.game.attempts < self.best_score:
                self.best_score = self.game.attempts
                self.update_stats()

        elif result in (GuessResult.OUT_OF_BOUNDS, GuessResult.ALREADY_GUESSED):
            self.set_feedback_state("low", "⚠️", msg)

    def append_history(self, text: str):
        self.txt_history.insert(tk.END, text + "\n")
        self.txt_history.see(tk.END)

    def clear_history(self):
        self.txt_history.delete("1.0", tk.END)


def launch_gui():
    root = tk.Tk()
    app = GuessingGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
