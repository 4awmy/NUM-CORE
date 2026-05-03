import customtkinter as ctk
import numpy as np
from numcore_gui.visualization import PlotManager
from numcore_gui.equation_input import EquationInputWidget
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider
from numcore_engine.parser import SymbolicParser
from numcore_engine.solvers.calculus_engine import (
    TrapezoidalSolver,
    SimpsonsRuleSolver,
    MidpointSolver,
    GaussianQuadratureSolver,
    NumericalDifferentiationSolver
)

class CalculusPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Ch 3: Numerical Calculus", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Help button next to title
        self.help_button = HelpProvider.create_help_button(self.input_frame, "calculus")
        self.help_button.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        # Method Selection
        self.method_label = ctk.CTkLabel(self.input_frame, text="Select Method:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        self.method_menu = ctk.CTkOptionMenu(
            self.input_frame, 
            values=[
                "Trapezoidal Rule", 
                "Simpson's 1/3", 
                "Simpson's 3/8", 
                "Midpoint Rule", 
                "Gaussian Quadrature",
                "Differentiation"
            ],
            command=self.update_inputs
        )
        self.method_menu.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Equation
        self.func_input = EquationInputWidget(self.input_frame)
        self.func_input.grid(row=3, column=0, padx=15, pady=(10, 0), sticky="ew")
        self.func_input.set_expression("x**2")

        # Range / Point
        self.range_label = ctk.CTkLabel(self.input_frame, text="Range [a, b]:")
        self.range_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.range_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 0, 1")
        self.range_entry.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.range_entry.insert(0, "0, 1")

        # Intervals / Step Size
        self.n_label = ctk.CTkLabel(self.input_frame, text="Intervals (n):")
        self.n_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.n_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 10")
        self.n_entry.grid(row=8, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.n_entry.insert(0, "10")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Solve", command=self.solve_action)
        self.solve_button.grid(row=9, column=0, padx=20, pady=20)


        # Results area
        self.results_panel = ctk.CTkFrame(self.input_frame, corner_radius=5, fg_color=("gray85", "gray15"))
        self.results_panel.grid(row=10, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="No data computed yet.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Inline Error Display
        self.error_label = ctk.CTkLabel(self.input_frame, text="", text_color="red", font=ctk.CTkFont(size=11))
        self.error_label.grid(row=11, column=0, padx=20, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Function Visualization", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)

        # Solvers mapping
        self.solvers = {
            "Trapezoidal Rule": TrapezoidalSolver(),
            "Simpson's 1/3": SimpsonsRuleSolver(),
            "Simpson's 3/8": SimpsonsRuleSolver(),
            "Midpoint Rule": MidpointSolver(),
            "Gaussian Quadrature": GaussianQuadratureSolver(),
            "Differentiation": NumericalDifferentiationSolver()
        }

    def update_inputs(self, method):
        """Updates the input fields based on the selected method."""
        if method == "Differentiation":
            self.range_label.configure(text="Point (x):")
            self.range_entry.delete(0, "end")
            self.range_entry.insert(0, "1.0")
            self.n_label.configure(text="Step Size (h):")
            self.n_entry.delete(0, "end")
            self.n_entry.insert(0, "0.001")
        elif method == "Gaussian Quadrature":
            self.range_label.configure(text="Range [a, b]:")
            self.n_label.configure(text="Points (2 or 3):")
            self.n_entry.delete(0, "end")
            self.n_entry.insert(0, "2")
        else:
            self.range_label.configure(text="Range [a, b]:")
            self.n_label.configure(text="Intervals (n):")
            if "Simpson" in method:
                self.n_entry.delete(0, "end")
                self.n_entry.insert(0, "6" if "3/8" in method else "10")

    def solve_action(self):
        """Triggers the numerical calculus solver and updates the plot."""
        self.error_label.configure(text="")
        if not self.func_input.is_valid():
            return

        method = self.method_menu.get()
        expression = self.func_input.get_expression()

        try:
            f = SymbolicParser.parse_expression(expression)
            solver = self.solvers[method]
            
            if method == "Differentiation":
                x = float(self.range_entry.get())
                h = float(self.n_entry.get())
                data = solver.solve(f=f, x=x, h=h, method="central")
                
                res = data.metadata.get("derivative")
                self.result_label.configure(text=f"Derivative at x={x}: {res:.6f}")
                
                # Use the new derivative tangent plot
                self.plot_manager.plot_derivative_tangent(expression, x, res)
                
            elif method == "Gaussian Quadrature":
                r_str = self.range_entry.get()
                a, b = map(float, r_str.split(","))
                pts = int(self.n_entry.get())
                data = solver.solve(f=f, a=a, b=b, points=pts)
                
                res = data.metadata.get("total_integral")
                self.result_label.configure(text=f"Integral from {a} to {b}: {res:.6f}")
                
                # Use the new integration area plot
                self.plot_manager.plot_integration_area(expression, a, b, method)
                
            else:
                r_str = self.range_entry.get()
                a, b = map(float, r_str.split(","))
                n = int(self.n_entry.get())
                
                kwargs = {"f": f, "a": a, "b": b, "n": n}
                if "Simpson" in method:
                    kwargs["method"] = "1/3" if "1/3" in method else "3/8"
                
                data = solver.solve(**kwargs)
                res = data.metadata.get("total_integral")
                self.result_label.configure(text=f"Integral from {a} to {b}: {res:.6f}")
                
                # Use the new integration area plot
                self.plot_manager.plot_integration_area(expression, a, b, method)

        except Exception as e:
            self.error_label.configure(text=f"Error: {str(e)}")
