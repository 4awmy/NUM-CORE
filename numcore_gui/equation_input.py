import customtkinter as ctk
from typing import Optional, Callable
import sympy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numcore_engine.parser import SymbolicParser
from numcore_gui import theme

class EquationInputWidget(ctk.CTkFrame):
    """
    A reusable widget for mathematical equation input with validation, 
    live MathText preview, and a symbol toolbar.
    """
    def __init__(
        self, 
        master, 
        label_text: str = "Equation f(x):", 
        placeholder: str = "e.g., x**2 - 4",
        on_change: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(master, fg_color=theme.get_panel_color(), **kwargs)
        
        self.on_change = on_change
        self._debounce_timer = None
        
        self.grid_columnconfigure(0, weight=1)
        
        # Label
        self.label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(weight="bold"))
        self.label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
        
        # Symbol Toolbar
        self.toolbar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 0))
        
        symbols = [
            ("sin", "sin()"), ("cos", "cos()"), ("tan", "tan()"), 
            ("ln", "ln()"), ("exp", "exp()"), ("sqrt", "sqrt()"), 
            ("π", "pi"), ("e", "E")
        ]
        
        for i, (label, val) in enumerate(symbols):
            btn = ctk.CTkButton(
                self.toolbar_frame, text=label, width=40, height=24,
                command=lambda v=val: self._insert_symbol(v)
            )
            btn.grid(row=0, column=i, padx=2)

        # Entry
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        self.entry.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.entry.bind("<KeyRelease>", self._handle_change)
        
        # Error Label
        self.error_label = ctk.CTkLabel(
            self, 
            text="", 
            text_color="#f44336", 
            font=ctk.CTkFont(size=11),
            height=0
        )
        self.error_label.grid(row=3, column=0, sticky="w", padx=5)

        # Preview Canvas
        self.preview_frame = ctk.CTkFrame(self, height=60, fg_color=theme.get_bg_color())
        self.preview_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.preview_frame.grid_propagate(False)
        
        self.fig = Figure(figsize=(4, 0.6), dpi=100, facecolor=theme.get_bg_color())
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')
        self.ax.set_facecolor(theme.get_bg_color())
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.preview_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.get_tk_widget().configure(bg=theme.get_bg_color())


    def _insert_symbol(self, symbol: str):
        """Inserts a symbol at the current cursor position."""
        pos = self.entry.index("insert")
        self.entry.insert(pos, symbol)
        # If it's a function, move cursor inside parentheses
        if "()" in symbol:
            self.entry.icursor(pos + symbol.find("(") + 1)
        self.entry.focus()
        self._handle_change()

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
        self._update_preview()

    def is_valid(self) -> bool:
        """Validates the current expression."""
        expr = self.get_expression()
        if not expr:
            self.show_error("Expression cannot be empty")
            return False
        try:
            valid = SymbolicParser.validate(expr)
            if valid:
                self.clear_error()
                return True
            else:
                self.show_error("Invalid expression")
                return False
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
        """Handles entry changes with debouncing."""
        if self._debounce_timer:
            self.after_cancel(self._debounce_timer)
        
        self._debounce_timer = self.after(300, self._process_change)

    def _process_change(self):
        """Processes the change after debounce delay."""
        expr = self.get_expression()
        self._update_preview()
        if self.on_change:
            self.on_change(expr)

    def _update_preview(self):
        """Updates the MathText preview."""
        expr_str = self.get_expression()
        self.ax.clear()
        self.ax.axis('off')
        
        if not expr_str:
            self.canvas.draw()
            return

        try:
            sym_expr = sympy.sympify(expr_str)
            latex_str = sympy.latex(sym_expr)
            if latex_str:
                self.ax.text(0.5, 0.5, f"${latex_str}$", 
                            fontsize=14, color='white', 
                            ha='center', va='center',
                            transform=self.ax.transAxes)
                self.clear_error()
        except Exception:
            # Don't show error immediately in preview to avoid flickering while typing
            pass
            
        self.canvas.draw()
