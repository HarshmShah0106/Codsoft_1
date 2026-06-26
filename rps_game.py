"""
Rock Paper Scissors - Modern GUI Game
--------------------------------------
A Tkinter-based Rock Paper Scissors game with a dark, modern aesthetic.

Rules:
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
- First player to reach WINNING_SCORE round wins takes the match.

Run with: python3 rps_game.py
"""

import tkinter as tk
from tkinter import font as tkfont
import random

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WINNING_SCORE = 5  # First to this many round-wins takes the match

CHOICES = ["rock", "paper", "scissors"]
EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

# Beats[a] = b  means a beats b
BEATS = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}

# ---------------------------------------------------------------------------
# Color palette - modern dark theme
# ---------------------------------------------------------------------------
BG = "#121212"
PANEL = "#1c1c1e"
PANEL_ALT = "#232327"
ACCENT = "#7c5cff"        # purple accent
ACCENT_HOVER = "#9b80ff"
WIN_COLOR = "#3ddc84"      # green
LOSE_COLOR = "#ff5c5c"     # red
TIE_COLOR = "#ffc857"      # amber
TEXT_PRIMARY = "#f5f5f7"
TEXT_SECONDARY = "#9a9aa2"
BORDER = "#2e2e33"


class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock · Paper · Scissors")
        self.root.geometry("560x680")
        self.root.minsize(480, 620)
        self.root.configure(bg=BG)

        # --- Fonts ---
        self.font_title = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.font_subtitle = tkfont.Font(family="Helvetica", size=11)
        self.font_score = tkfont.Font(family="Helvetica", size=34, weight="bold")
        self.font_score_label = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.font_choice_emoji = tkfont.Font(family="Helvetica", size=42)
        self.font_choice_label = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.font_result = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.font_vs = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.font_button = tkfont.Font(family="Helvetica", size=13, weight="bold")
        self.font_status = tkfont.Font(family="Helvetica", size=10)

        # --- State ---
        self.user_score = 0
        self.computer_score = 0
        self.round_number = 1
        self.match_over = False

        self._build_ui()

    # -------------------------------------------------------------------
    # UI construction
    # -------------------------------------------------------------------
    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", pady=(24, 10), padx=24)

        tk.Label(
            header, text="Rock · Paper · Scissors",
            font=self.font_title, fg=TEXT_PRIMARY, bg=BG
        ).pack()
        self.subtitle_label = tk.Label(
            header, text=f"First to {WINNING_SCORE} wins the match",
            font=self.font_subtitle, fg=TEXT_SECONDARY, bg=BG
        )
        self.subtitle_label.pack(pady=(4, 0))

        # Scoreboard
        score_frame = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER,
                                highlightthickness=1)
        score_frame.pack(fill="x", padx=24, pady=(16, 10))

        you_box = tk.Frame(score_frame, bg=PANEL)
        you_box.pack(side="left", expand=True, fill="both", pady=14)
        tk.Label(you_box, text="YOU", font=self.font_score_label,
                 fg=ACCENT, bg=PANEL).pack()
        self.user_score_label = tk.Label(
            you_box, text="0", font=self.font_score, fg=TEXT_PRIMARY, bg=PANEL
        )
        self.user_score_label.pack()

        tk.Frame(score_frame, bg=BORDER, width=1).pack(side="left", fill="y", pady=10)

        round_box = tk.Frame(score_frame, bg=PANEL)
        round_box.pack(side="left", expand=True, fill="both", pady=14)
        tk.Label(round_box, text="ROUND", font=self.font_score_label,
                 fg=TEXT_SECONDARY, bg=PANEL).pack()
        self.round_label = tk.Label(
            round_box, text="1", font=self.font_score, fg=TEXT_SECONDARY, bg=PANEL
        )
        self.round_label.pack()

        tk.Frame(score_frame, bg=BORDER, width=1).pack(side="left", fill="y", pady=10)

        cpu_box = tk.Frame(score_frame, bg=PANEL)
        cpu_box.pack(side="left", expand=True, fill="both", pady=14)
        tk.Label(cpu_box, text="COMPUTER", font=self.font_score_label,
                 fg=LOSE_COLOR, bg=PANEL).pack()
        self.cpu_score_label = tk.Label(
            cpu_box, text="0", font=self.font_score, fg=TEXT_PRIMARY, bg=PANEL
        )
        self.cpu_score_label.pack()

        # Battle display (choices shown after a pick)
        battle_frame = tk.Frame(self.root, bg=BG)
        battle_frame.pack(fill="x", padx=24, pady=(14, 6))

        self.user_choice_panel = self._make_choice_panel(battle_frame, "YOU")
        self.user_choice_panel["frame"].pack(side="left", expand=True, fill="both", padx=(0, 8))

        tk.Label(battle_frame, text="VS", font=self.font_vs,
                 fg=TEXT_SECONDARY, bg=BG).pack(side="left", padx=4)

        self.cpu_choice_panel = self._make_choice_panel(battle_frame, "COMPUTER")
        self.cpu_choice_panel["frame"].pack(side="left", expand=True, fill="both", padx=(8, 0))

        # Result banner
        self.result_label = tk.Label(
            self.root, text="Make your move!",
            font=self.font_result, fg=TEXT_SECONDARY, bg=BG
        )
        self.result_label.pack(pady=(14, 6))

        # Choice buttons
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=(8, 10))

        self.choice_buttons = {}
        for choice in CHOICES:
            btn = self._make_choice_button(btn_frame, choice)
            btn.pack(side="left", padx=10)
            self.choice_buttons[choice] = btn

        # Status / controls
        controls = tk.Frame(self.root, bg=BG)
        controls.pack(pady=(6, 4))

        self.play_again_btn = tk.Button(
            controls, text="🔄  New Match", font=self.font_button,
            bg=PANEL_ALT, fg=TEXT_PRIMARY, activebackground=BORDER,
            activeforeground=TEXT_PRIMARY, relief="flat", bd=0,
            padx=18, pady=8, cursor="hand2",
            command=self.reset_match
        )
        self.play_again_btn.pack()

        self.status_label = tk.Label(
            self.root, text="", font=self.font_status,
            fg=TEXT_SECONDARY, bg=BG
        )
        self.status_label.pack(pady=(10, 16))

    def _make_choice_panel(self, parent, title):
        frame = tk.Frame(parent, bg=PANEL_ALT, highlightbackground=BORDER,
                          highlightthickness=1, height=130)
        frame.pack_propagate(False)

        title_label = tk.Label(frame, text=title, font=self.font_choice_label,
                                fg=TEXT_SECONDARY, bg=PANEL_ALT)
        title_label.pack(pady=(10, 0))

        emoji_label = tk.Label(frame, text="❔", font=self.font_choice_emoji,
                                fg=TEXT_PRIMARY, bg=PANEL_ALT)
        emoji_label.pack(expand=True)

        name_label = tk.Label(frame, text="—", font=self.font_choice_label,
                               fg=TEXT_SECONDARY, bg=PANEL_ALT)
        name_label.pack(pady=(0, 10))

        return {"frame": frame, "emoji": emoji_label, "name": name_label}

    def _make_choice_button(self, parent, choice):
        btn = tk.Button(
            parent,
            text=f"{EMOJI[choice]}\n{choice.capitalize()}",
            font=self.font_choice_label,
            bg=PANEL_ALT, fg=TEXT_PRIMARY,
            activebackground=ACCENT, activeforeground="#ffffff",
            relief="flat", bd=0,
            width=8, height=4,
            cursor="hand2",
            command=lambda c=choice: self.play_round(c)
        )
        # Hover effects
        btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, True))
        btn.bind("<Leave>", lambda e, b=btn: self._on_hover(b, False))
        return btn

    def _on_hover(self, btn, entering):
        if str(btn["state"]) == "disabled":
            return
        btn.configure(bg=ACCENT_HOVER if entering else PANEL_ALT)

    # -------------------------------------------------------------------
    # Game logic
    # -------------------------------------------------------------------
    def play_round(self, user_choice):
        if self.match_over:
            return

        computer_choice = random.choice(CHOICES)

        # Update display panels
        self._set_choice_panel(self.user_choice_panel, user_choice)
        self._set_choice_panel(self.cpu_choice_panel, computer_choice)

        outcome = self._determine_winner(user_choice, computer_choice)

        if outcome == "win":
            self.user_score += 1
            self.result_label.config(text="🎉 You win this round!", fg=WIN_COLOR)
        elif outcome == "lose":
            self.computer_score += 1
            self.result_label.config(text="💥 Computer wins this round!", fg=LOSE_COLOR)
        else:
            self.result_label.config(text="🤝 It's a tie!", fg=TIE_COLOR)

        self.user_score_label.config(text=str(self.user_score))
        self.cpu_score_label.config(text=str(self.computer_score))

        # Check for match winner
        if self.user_score >= WINNING_SCORE or self.computer_score >= WINNING_SCORE:
            self._end_match()
        else:
            self.round_number += 1
            self.round_label.config(text=str(self.round_number))
            self.status_label.config(
                text=f"Choose rock, paper, or scissors for round {self.round_number}."
            )

    def _determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "tie"
        if BEATS[user_choice] == computer_choice:
            return "win"
        return "lose"

    def _set_choice_panel(self, panel, choice):
        panel["emoji"].config(text=EMOJI[choice])
        panel["name"].config(text=choice.capitalize())

    def _end_match(self):
        self.match_over = True
        for btn in self.choice_buttons.values():
            btn.config(state="disabled", bg=PANEL)

        if self.user_score > self.computer_score:
            self.result_label.config(
                text=f"🏆 You won the match {self.user_score}-{self.computer_score}!",
                fg=WIN_COLOR
            )
        else:
            self.result_label.config(
                text=f"☠️ Computer won the match {self.computer_score}-{self.user_score}!",
                fg=LOSE_COLOR
            )
        self.status_label.config(text="Click 'New Match' to play again.")

    def reset_match(self):
        self.user_score = 0
        self.computer_score = 0
        self.round_number = 1
        self.match_over = False

        self.user_score_label.config(text="0")
        self.cpu_score_label.config(text="0")
        self.round_label.config(text="1")

        self._set_choice_panel(self.user_choice_panel, None) if False else None
        self.user_choice_panel["emoji"].config(text="❔")
        self.user_choice_panel["name"].config(text="—")
        self.cpu_choice_panel["emoji"].config(text="❔")
        self.cpu_choice_panel["name"].config(text="—")

        self.result_label.config(text="Make your move!", fg=TEXT_SECONDARY)
        self.status_label.config(text="")

        for btn in self.choice_buttons.values():
            btn.config(state="normal", bg=PANEL_ALT)


def main():
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
