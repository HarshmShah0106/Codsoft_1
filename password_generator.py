"""
Password Generator - Modern GUI Application
---------------------------------------------
A Tkinter-based password generator with adjustable length, character-type
selection, a strength meter, an option to exclude similar-looking
characters, and a one-click copy-to-clipboard button.

Run with: python3 password_generator.py
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import string

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MIN_LENGTH = 13
MAX_LENGTH = 64
DEFAULT_LENGTH = 16

# Characters that look similar/ambiguous and can be optionally excluded
SIMILAR_CHARS = "il1Lo0O"

# ---------------------------------------------------------------------------
# Color palette - dark theme (matches the RPS game style)
# ---------------------------------------------------------------------------
BG = "#121212"
PANEL = "#1c1c1e"
PANEL_ALT = "#232327"
ACCENT = "#7c5cff"
ACCENT_HOVER = "#9b80ff"
WEAK_COLOR = "#ff5c5c"
MEDIUM_COLOR = "#ffc857"
STRONG_COLOR = "#3ddc84"
VERY_STRONG_COLOR = "#33b5e5"
TEXT_PRIMARY = "#f5f5f7"
TEXT_SECONDARY = "#9a9aa2"
BORDER = "#2e2e33"


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("480x680")
        self.root.minsize(420, 640)
        self.root.configure(bg=BG)

        # --- Fonts ---
        self.font_title = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.font_subtitle = tkfont.Font(family="Helvetica", size=11)
        self.font_section = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.font_password = tkfont.Font(family="Courier", size=15, weight="bold")
        self.font_checkbox = tkfont.Font(family="Helvetica", size=11)
        self.font_button = tkfont.Font(family="Helvetica", size=13, weight="bold")
        self.font_small = tkfont.Font(family="Helvetica", size=9)
        self.font_length_value = tkfont.Font(family="Helvetica", size=13, weight="bold")

        # --- State variables ---
        self.length_var = tk.IntVar(value=DEFAULT_LENGTH)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_similar = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar(value="")

        self._build_ui()
        self.generate_password()  # show one immediately on launch

    # -------------------------------------------------------------------
    # UI construction
    # -------------------------------------------------------------------
    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", pady=(24, 8), padx=24)

        tk.Label(
            header, text="🔐 Password Generator",
            font=self.font_title, fg=TEXT_PRIMARY, bg=BG
        ).pack()
        tk.Label(
            header, text="Create strong, random passwords instantly",
            font=self.font_subtitle, fg=TEXT_SECONDARY, bg=BG
        ).pack(pady=(4, 0))

        # Password display panel
        pw_frame = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER,
                             highlightthickness=1)
        pw_frame.pack(fill="x", padx=24, pady=(18, 8))

        self.password_entry = tk.Entry(
            pw_frame, textvariable=self.password_var,
            font=self.font_password, fg=TEXT_PRIMARY, bg=PANEL,
            relief="flat", justify="center", insertbackground=TEXT_PRIMARY,
            readonlybitmap="", state="readonly"
        )
        self.password_entry.pack(fill="x", padx=16, pady=(18, 6), ipady=6)

        # Strength meter
        strength_frame = tk.Frame(pw_frame, bg=PANEL)
        strength_frame.pack(fill="x", padx=16, pady=(0, 16))

        self.strength_canvas = tk.Canvas(
            strength_frame, height=8, bg=PANEL_ALT,
            highlightthickness=0
        )
        self.strength_canvas.pack(fill="x", pady=(0, 6))

        self.strength_label = tk.Label(
            strength_frame, text="", font=self.font_small,
            fg=TEXT_SECONDARY, bg=PANEL
        )
        self.strength_label.pack(anchor="w")

        # Copy button (below password panel)
        self.copy_btn = tk.Button(
            self.root, text="📋  Copy to Clipboard", font=self.font_button,
            bg=PANEL_ALT, fg=TEXT_PRIMARY, activebackground=BORDER,
            activeforeground=TEXT_PRIMARY, relief="flat", bd=0,
            padx=14, pady=8, cursor="hand2",
            command=self.copy_to_clipboard
        )
        self.copy_btn.pack(padx=24, fill="x", pady=(0, 16))

        # Options panel
        options_frame = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER,
                                  highlightthickness=1)
        options_frame.pack(fill="x", padx=24, pady=(0, 16))

        # Length control
        length_section = tk.Frame(options_frame, bg=PANEL)
        length_section.pack(fill="x", padx=18, pady=(16, 10))

        length_header = tk.Frame(length_section, bg=PANEL)
        length_header.pack(fill="x")
        tk.Label(length_header, text="PASSWORD LENGTH", font=self.font_section,
                 fg=TEXT_SECONDARY, bg=PANEL).pack(side="left")
        self.length_value_label = tk.Label(
            length_header, text=str(DEFAULT_LENGTH), font=self.font_length_value,
            fg=ACCENT, bg=PANEL
        )
        self.length_value_label.pack(side="right")

        self.length_scale = tk.Scale(
            length_section, from_=MIN_LENGTH, to=MAX_LENGTH,
            orient="horizontal", variable=self.length_var,
            command=self._on_length_change,
            bg=PANEL, fg=TEXT_PRIMARY, troughcolor=PANEL_ALT,
            highlightthickness=0, bd=0, sliderrelief="flat",
            activebackground=ACCENT, showvalue=False
        )
        self.length_scale.pack(fill="x", pady=(8, 0))

        tk.Label(
            length_section, text=f"Minimum {MIN_LENGTH} characters recommended for strong security",
            font=self.font_small, fg=TEXT_SECONDARY, bg=PANEL
        ).pack(anchor="w", pady=(6, 0))

        # Divider
        tk.Frame(options_frame, bg=BORDER, height=1).pack(fill="x", padx=18, pady=(6, 12))

        # Character type checkboxes
        char_section = tk.Frame(options_frame, bg=PANEL)
        char_section.pack(fill="x", padx=18, pady=(0, 6))

        tk.Label(char_section, text="INCLUDE CHARACTERS", font=self.font_section,
                 fg=TEXT_SECONDARY, bg=PANEL).pack(anchor="w", pady=(0, 8))

        self._make_checkbox(char_section, "Uppercase letters (A-Z)", self.use_upper)
        self._make_checkbox(char_section, "Lowercase letters (a-z)", self.use_lower)
        self._make_checkbox(char_section, "Numbers (0-9)", self.use_digits)
        self._make_checkbox(char_section, "Symbols (!@#$%^&*)", self.use_symbols)

        tk.Frame(options_frame, bg=BORDER, height=1).pack(fill="x", padx=18, pady=(6, 12))

        exclude_section = tk.Frame(options_frame, bg=PANEL)
        exclude_section.pack(fill="x", padx=18, pady=(0, 16))
        self._make_checkbox(
            exclude_section,
            "Exclude similar-looking characters (l, 1, I, O, 0)",
            self.exclude_similar
        )

        # Generate button
        self.generate_btn = tk.Button(
            self.root, text="⚡  Generate Password", font=self.font_button,
            bg=ACCENT, fg="#ffffff", activebackground=ACCENT_HOVER,
            activeforeground="#ffffff", relief="flat", bd=0,
            padx=18, pady=12, cursor="hand2",
            command=self.generate_password
        )
        self.generate_btn.pack(padx=24, fill="x")
        self.generate_btn.bind("<Enter>", lambda e: self.generate_btn.config(bg=ACCENT_HOVER))
        self.generate_btn.bind("<Leave>", lambda e: self.generate_btn.config(bg=ACCENT))

        # Status label (for copy confirmation / errors)
        self.status_label = tk.Label(
            self.root, text="", font=self.font_small,
            fg=TEXT_SECONDARY, bg=BG
        )
        self.status_label.pack(pady=(12, 16))

    def _make_checkbox(self, parent, text, variable):
        cb = tk.Checkbutton(
            parent, text=text, variable=variable,
            font=self.font_checkbox, fg=TEXT_PRIMARY, bg=PANEL,
            activebackground=PANEL, activeforeground=TEXT_PRIMARY,
            selectcolor=PANEL_ALT, relief="flat", bd=0,
            highlightthickness=0, anchor="w", cursor="hand2",
            command=self.generate_password
        )
        cb.pack(fill="x", pady=3)
        return cb

    def _on_length_change(self, value):
        self.length_value_label.config(text=str(int(float(value))))
        self.generate_password()

    # -------------------------------------------------------------------
    # Password generation logic
    # -------------------------------------------------------------------
    def _build_character_pool(self):
        pool = ""
        if self.use_upper.get():
            pool += string.ascii_uppercase
        if self.use_lower.get():
            pool += string.ascii_lowercase
        if self.use_digits.get():
            pool += string.digits
        if self.use_symbols.get():
            pool += "!@#$%^&*()-_=+[]{};:,.?/"

        if self.exclude_similar.get():
            pool = "".join(ch for ch in pool if ch not in SIMILAR_CHARS)

        return pool

    def generate_password(self):
        pool = self._build_character_pool()
        length = self.length_var.get()

        if not pool:
            self.password_var.set("")
            self.status_label.config(
                text="⚠️ Select at least one character type.", fg=WEAK_COLOR
            )
            self._draw_strength_bar(0)
            self.strength_label.config(text="")
            return

        # Build a guaranteed-diverse password: include at least one char
        # from each selected category, then fill the rest randomly.
        required_chars = []
        if self.use_upper.get():
            required_chars.append(random.choice(self._filtered(string.ascii_uppercase)))
        if self.use_lower.get():
            required_chars.append(random.choice(self._filtered(string.ascii_lowercase)))
        if self.use_digits.get():
            required_chars.append(random.choice(self._filtered(string.digits)))
        if self.use_symbols.get():
            required_chars.append(random.choice(self._filtered("!@#$%^&*()-_=+[]{};:,.?/")))

        # If length is shorter than the number of required categories,
        # just sample randomly from the pool (rare edge case).
        if length < len(required_chars):
            password = "".join(random.choice(pool) for _ in range(length))
        else:
            remaining = length - len(required_chars)
            password_chars = required_chars + [random.choice(pool) for _ in range(remaining)]
            random.shuffle(password_chars)
            password = "".join(password_chars)

        self.password_var.set(password)
        self.status_label.config(text="")
        self._update_strength_meter(password)

    def _filtered(self, charset):
        """Apply the exclude-similar filter to a given charset, falling
        back to the original set if filtering would empty it."""
        if self.exclude_similar.get():
            filtered = "".join(ch for ch in charset if ch not in SIMILAR_CHARS)
            return filtered if filtered else charset
        return charset

    # -------------------------------------------------------------------
    # Strength meter
    # -------------------------------------------------------------------
    def _score_password(self, password):
        """Simple heuristic strength score from 0-100."""
        length = len(password)
        categories = sum([
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(c in "!@#$%^&*()-_=+[]{};:,.?/" for c in password),
        ])

        # Length contributes up to 60 points, variety up to 40 points
        length_score = min(length / 24, 1.0) * 60
        variety_score = (categories / 4) * 40
        return round(length_score + variety_score)

    def _update_strength_meter(self, password):
        score = self._score_password(password)

        if score < 35:
            label, color = "Weak", WEAK_COLOR
        elif score < 60:
            label, color = "Medium", MEDIUM_COLOR
        elif score < 85:
            label, color = "Strong", STRONG_COLOR
        else:
            label, color = "Very Strong", VERY_STRONG_COLOR

        self.strength_label.config(text=f"Strength: {label}", fg=color)
        self._draw_strength_bar(score, color)

    def _draw_strength_bar(self, score, color=PANEL_ALT):
        self.strength_canvas.delete("all")
        width = self.strength_canvas.winfo_width() or 380
        height = 8
        fill_width = int((score / 100) * width)

        # Background track
        self.strength_canvas.create_rectangle(
            0, 0, width, height, fill=PANEL_ALT, outline=""
        )
        # Filled portion
        if fill_width > 0:
            self.strength_canvas.create_rectangle(
                0, 0, fill_width, height, fill=color, outline=""
            )

    # -------------------------------------------------------------------
    # Clipboard
    # -------------------------------------------------------------------
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if not password:
            self.status_label.config(text="⚠️ No password to copy.", fg=WEAK_COLOR)
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()  # ensures clipboard persists after app focus changes

        self.status_label.config(text="✅ Password copied to clipboard!", fg=STRONG_COLOR)
        # Clear the confirmation message after a couple seconds
        self.root.after(2000, lambda: self.status_label.config(text=""))


def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    # Redraw the strength bar correctly once the window has its real size
    root.after(50, lambda: app._draw_strength_bar(
        app._score_password(app.password_var.get()),
        app.strength_label.cget("fg")
    ))
    root.mainloop()


if __name__ == "__main__":
    main()
