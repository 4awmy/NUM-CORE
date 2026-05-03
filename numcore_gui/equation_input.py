import customtkinter as ctk
from typing import Optional, Callable
from numcore_engine.parser import SymbolicParser

class EquationInputWidget(ctk.CTkFrame):
    """
    A reusable widget for mathematical equation input with validation and error display.
    """
    def __init__(
        self, 
        master, 
        label_text: str = "Equation f(x):", 
        placeholder: str = "e.g., x**2 - 4",
        on_change: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.on_change = on_change
        self.grid_columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(weight="bold"))
        self.label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
        
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        self.entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.entry.bind("<KeyRelease>", self._handle_change)
        
        self.error_label = ctk.CTkLabel(
            self, 
            text="", 
            text_color="#f44336", 
            font=ctk.CTkFont(size=11),
            height=0
        )
        self.error_label.grid(row=2, column=0, sticky="w", padx=5)

    def get_expression(self) -> str:
        """Returns the cleaned expression string."""
        return self.entry.get().strip()

    def get_raw(self) -> str:
        """Returns the raw entry content."""
        return self.entry.get()

    def set_expression(self, expr: str):
        """Sets the entry content."""
        self.entry.delete(0, "end")
        self.entry.insert(0, expr)
        self.clear_error()

    def is_valid(self) -> bool:
        """Validates the current expression."""
        expr = self.get_expression()
        if not expr:
            self.show_error("Expression cannot be empty")
            return False
        try:
            SymbolicParser.parse_expression(expr)
            self.clear_error()
            return True
        except Exception as e:
            self.show_error(str(e))
            return False

    def show_error(self, msg: str):
        """Displays an error message below the input."""
        self.error_label.configure(text=msg)
        self.entry.configure(border_color="#f44336")

    def clear_error(self):
        """Clears any displayed error."""
        self.error_label.configure(text="")
        self.entry.configure(border_color=["#979DA2", "#565B5E"]) # Default CTk colors

    def _handle_change(self, event=None):
        if self.on_change:
            self.on_change(self.get_expression())
