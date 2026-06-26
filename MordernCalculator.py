import tkinter as tk

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("320x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50") # Dark background

        # Current expression state
        self.expression = ""
        self.display_var = tk.StringVar()
        self.display_var.set("0")

        self._build_ui()

    def _build_ui(self):
        # --- Display Screen ---
        display_frame = tk.Frame(self.root, bg="#2c3e50")
        display_frame.pack(expand=True, fill="both", padx=10, pady=20)

        display_label = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            anchor="e",       # Align text to the right
            bg="#ecf0f1",     # Light display background
            fg="#2c3e50",     # Dark text
            font=("Helvetica", 28, "bold"), 
            padx=15, 
            pady=10,
            relief="flat"
        )
        display_label.pack(expand=True, fill="both")

        # --- Buttons ---
        buttons_frame = tk.Frame(self.root, bg="#2c3e50")
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        # Button Layout Grid
        button_layout = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        # Colors for smooth UI
        num_bg, num_fg = "#34495e", "#ffffff"
        op_bg, op_fg = "#e67e22", "#ffffff"
        clear_bg, clear_fg = "#e74c3c", "#ffffff"
        eq_bg, eq_fg = "#27ae60", "#ffffff"

        for (text, row, col) in button_layout:
            # Determine styling based on button type
            if text in ['/', '*', '-', '+']:
                bg_color, fg_color = op_bg, op_fg
            elif text == 'C':
                bg_color, fg_color = clear_bg, clear_fg
            elif text == '=':
                bg_color, fg_color = eq_bg, eq_fg
            else:
                bg_color, fg_color = num_bg, num_fg

            button = tk.Button(
                buttons_frame, 
                text=text, 
                font=("Helvetica", 16, "bold"), 
                bg=bg_color, 
                fg=fg_color, 
                activebackground="#95a5a6", # Color when clicked
                borderwidth=0,
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

            # Configure dynamic grid sizing
            buttons_frame.rowconfigure(row, weight=1)
            buttons_frame.columnconfigure(col, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            # Clear everything
            self.expression = ""
            self.display_var.set("0")
            
        elif char == '=':
            # Calculate the result
            try:
                # evaluate the math expression
                result = str(eval(self.expression))
                
                # Format to remove trailing .0 for clean integers
                if result.endswith(".0"):
                    result = result[:-2]
                    
                self.display_var.set(result)
                self.expression = result # allow continuing math on the result
                
            except ZeroDivisionError:
                self.display_var.set("Div by Zero")
                self.expression = ""
            except Exception:
                self.display_var.set("Error")
                self.expression = ""
                
        else:
            # Prevent leading zeros from stacking
            if self.expression == "" and char == '0':
                return
            
            self.expression += str(char)
            self.display_var.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()
