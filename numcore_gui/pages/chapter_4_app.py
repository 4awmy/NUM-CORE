import customtkinter as ctk
import numpy as np
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_engine.solvers.calculus_engine import (
    IntegrationSolver,
    TrapezoidalSolver,
    SimpsonsRuleSolver,
    GaussianQuadratureSolver
)
from numcore_engine.parser import SymbolicParser
from numcore_gui.equation_input import EquationInputWidget
from numcore_gui.smart_solver_panel import SmartSolverPanel

class Chapter4AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Problem & Inputs
        self.input_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Chapter 4 Application: Numerical Calculus", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Problem Statement
        self.problem_text = (
            "Application: Numerical Integration and Differentiation\n\n"
            "Numerical calculus methods are used to approximate integrals and "
            "derivatives of functions that are difficult to solve analytically. "
            "This application compares different integration techniques.\n\n"
            "Example Equation:\n"
            "f(x) = 50*x + 10*x^2"
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
            label_text="Function f(x):",
            placeholder="e.g., 50*x + 10*x**2"
        )
        self.func_input.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.func_input.set_expression("50*x + 10*x**2")

        self.a_label = ctk.CTkLabel(self.input_frame, text="Lower Limit (a):")
        self.a_label.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        self.a_entry = ctk.CTkEntry(self.input_frame)
        self.a_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.a_entry.insert(0, "0")

        self.b_label = ctk.CTkLabel(self.input_frame, text="Upper Limit (b):")
        self.b_label.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")
        self.b_entry = ctk.CTkEntry(self.input_frame)
        self.b_entry.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.b_entry.insert(0, "2")

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.button_frame.grid(row=8, column=0, padx=20, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.solve_button = ctk.CTkButton(self.button_frame, text="Solve", command=self.solve_action)
        self.solve_button.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        self.smart_solve_button = ctk.CTkButton(
            self.button_frame, 
            text="Smart Solve", 
            fg_color="#673AB7", 
            hover_color="#5E35B1",
            command=self.smart_solve_action
        )
        self.smart_solve_button.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="ew")

        # Results area
        self.results_panel = ctk.CTkFrame(self.input_frame, corner_radius=5, fg_color=("gray85", "gray15"))
        self.results_panel.grid(row=9, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="Click 'Solve' to begin.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Smart Solver Panel (Inline)
        self.smart_panel = SmartSolverPanel(self.input_frame)
        self.smart_panel.grid(row=10, column=0, padx=20, pady=10, sticky="nsew")
        self.smart_panel.grid_forget() # Hidden by default

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Function Plot (Area = Integral)", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)
        
        self.solvers = {
            "Simpson's 1/3": SimpsonsRuleSolver(),
            "Trapezoidal": TrapezoidalSolver(),
            "Gaussian Quadrature": GaussianQuadratureSolver()
        }

    def solve_action(self):
        self.smart_panel.grid_forget()
        if not self.func_input.is_valid():
            return

        expression = self.func_input.get_expression()
        a = float(self.a_entry.get())
        b = float(self.b_entry.get())
        
        try:
            f = SymbolicParser.parse_expression(expression)
            solver = self.solvers["Simpson's 1/3"]
            data = solver.solve(f=f, a=a, b=b, n=100, method="1/3")
            
            self.plot_manager.plot_integration_area(expression, a, b, "Simpson's 1/3")
            
            result = data.metadata.get("total_integral")
            self.result_label.configure(text=f"Integral Result:\n{result:.4f}")
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")

    def smart_solve_action(self):
        """Compares integration methods."""
        if not self.func_input.is_valid():
            return

        expression = self.func_input.get_expression()
        a = float(self.a_entry.get())
        b = float(self.b_entry.get())
        
        results = []
        try:
            f = SymbolicParser.parse_expression(expression)
            
            configs = [
                ("Simpson's 1/3", self.solvers["Simpson's 1/3"], {"n": 100, "method": "1/3"}),
                ("Trapezoidal", self.solvers["Trapezoidal"], {"n": 100}),
                ("Gaussian Quadrature", self.solvers["Gaussian Quadrature"], {"n": 5})
            ]

            for method_name, solver, extra_kwargs in configs:
                try:
                    kwargs = {"f": f, "a": a, "b": b}
                    kwargs.update(extra_kwargs)
                    data = solver.solve(**kwargs)
                    res = data.metadata.get("total_integral")
                    results.append({
                        "method": method_name,
                        "diverged": False,
                        "iterations": extra_kwargs.get("n", 0),
                        "error": 0.0,
                        "root": res,
                        "reason": "Integration completed."
                    })
                except Exception as e:
                    results.append({
                        "method": method_name,
                        "diverged": True,
                        "iterations": 0,
                        "error": 1.0,
                        "root": None,
                        "reason": str(e)
                    })

            self.smart_panel.grid(row=10, column=0, padx=20, pady=10, sticky="nsew")
            self.smart_panel.populate(results)
            self.solve_action()
            
        except Exception as e:
            self.result_label.configure(text=f"Smart Solve Error: {str(e)}")

