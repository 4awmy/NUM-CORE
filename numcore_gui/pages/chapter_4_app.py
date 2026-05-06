import customtkinter as ctk
import numpy as np
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_engine.solvers.calculus_engine import SimpsonsRuleSolver
from numcore_engine.parser import SymbolicParser
from numcore_gui.equation_input import EquationInputWidget
from numcore_gui import theme

class Chapter4AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.get_bg_color(), **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Problem & Inputs
        self.input_frame = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color=theme.get_panel_color(), border_color=theme.get_border_color(), border_width=1)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Work Done Computation", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Problem Statement
        self.problem_text = (
            "Problem: Computing Work Done by a Variable Force\n\n"
            "The work done W by a force F(x) moving an object from x=a to x=b is "
            "given by the integral of F(x) dx from a to b.\n\n"
            "Example: A spring force F(x) = 50*x + 10*x^2. Find the work done "
            "to compress the spring from x=0 to x=2 meters."
        )
        self.problem_label = ctk.CTkLabel(
            self.input_frame, 
            text=self.problem_text, 
            justify="left", 
            wraplength=350,
            font=ctk.CTkFont(size=12)
        )
        self.problem_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        # Pre-filled Example
        self.func_input = EquationInputWidget(
            self.input_frame, 
            label_text="Force Function F(x):",
            placeholder="e.g., 50*x + 10*x**2"
        )
        self.func_input.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.func_input.set_expression("50*x + 10*x**2")

        self.a_label = ctk.CTkLabel(self.input_frame, text="Start Position (a):")
        self.a_label.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        self.a_entry = ctk.CTkEntry(self.input_frame)
        self.a_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.a_entry.insert(0, "0")

        self.b_label = ctk.CTkLabel(self.input_frame, text="End Position (b):")
        self.b_label.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")
        self.b_entry = ctk.CTkEntry(self.input_frame)
        self.b_entry.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.b_entry.insert(0, "2")

        # Example problems dropdown
        self.example_label = ctk.CTkLabel(self.input_frame, text="Load Example:")
        self.example_label.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="w")
        self.example_menu = ctk.CTkOptionMenu(
            self.input_frame,
            values=["Spring Force (Default)", "Constant Force", "Quadratic Force", "Cubic Force"],
            command=self.load_example
        )
        self.example_menu.set("Spring Force (Default)")
        self.example_menu.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Solve Example", command=self.solve_action)
        self.solve_button.grid(row=10, column=0, padx=20, pady=20)

        # Results area
        self.results_panel = ctk.CTkFrame(self.input_frame, corner_radius=5, fg_color=theme.get_bg_color(), border_color=theme.get_border_color(), border_width=1)
        self.results_panel.grid(row=11, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="Click 'Solve' to begin.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=theme.get_panel_color(), border_color=theme.get_border_color(), border_width=1)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Force vs Distance (Area = Work)", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color=theme.get_bg_color(), corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)

        self.solver = SimpsonsRuleSolver()
        
        # Example problems
        self.examples = {
            "Spring Force (Default)": {
                "expression": "50*x + 10*x**2",
                "a": "0",
                "b": "2"
            },
            "Constant Force": {
                "expression": "100",
                "a": "0",
                "b": "5"
            },
            "Quadratic Force": {
                "expression": "x**2",
                "a": "0",
                "b": "4"
            },
            "Cubic Force": {
                "expression": "x**3",
                "a": "0",
                "b": "3"
            }
        }

    def load_example(self, example_name):
        """Load selected example into input fields."""
        if example_name in self.examples:
            example = self.examples[example_name]
            self.func_input.set_expression(example["expression"])
            self.a_entry.delete(0, ctk.END)
            self.a_entry.insert(0, example["a"])
            self.b_entry.delete(0, ctk.END)
            self.b_entry.insert(0, example["b"])

    def update_theme(self):
        """Update all widget colors when theme changes."""
        self.configure(fg_color=theme.get_bg_color())
        self.input_frame.configure(fg_color=theme.get_panel_color(), border_color=theme.get_border_color())
        self.results_panel.configure(fg_color=theme.get_bg_color(), border_color=theme.get_border_color())
        self.viz_frame.configure(fg_color=theme.get_panel_color(), border_color=theme.get_border_color())
        self.plot_placeholder.configure(fg_color=theme.get_bg_color())
        # Refresh the plot manager's theme
        if hasattr(self, 'plot_manager') and self.plot_manager:
            self.plot_manager._apply_dark_theme()
            self.plot_manager.canvas.draw()

    def solve_action(self):
        expression = self.func_input.get_expression()
        a = float(self.a_entry.get())
        b = float(self.b_entry.get())
        
        try:
            import time
            start_time = time.perf_counter()

            f = SymbolicParser.parse_expression(expression)
            data = self.solver.solve(f=f, a=a, b=b, n=100, method="1/3")
            
            end_time = time.perf_counter()
            comp_time = end_time - start_time

            # Update Dashboard status
            if hasattr(self.master.master, "update_status"):
                self.master.master.update_status("Work Done Solver", comp_time)

            self.plot_manager.plot_integration_area(expression, a, b, "Simpson's 1/3")
            
            result = data.metadata.get("total_integral")
            self.result_label.configure(text=f"Total Work Done:\n{result:.4f} Joules")
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")
