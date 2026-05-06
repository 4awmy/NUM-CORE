import customtkinter as ctk
import numpy as np
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui import theme
from numcore_gui.result_panel import ResultPanel
from numcore_gui.help_system import HelpProvider
from numcore_engine.parser import SymbolicParser
from numcore_engine.solvers.calculus_engine import (
    TrapezoidalSolver,
    SimpsonsRuleSolver,
    MidpointSolver,
    GaussianQuadratureSolver,
    NumericalDifferentiationSolver
)
from numcore_engine.solvers.comparison import ComparisonRunner
from numcore_gui.smart_solver_panel import SmartSolverPanel

from numcore_gui.equation_input import EquationInputWidget

class CalculusPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.get_bg_color(), **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Inputs
        self.input_frame = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color=theme.get_panel_color(), border_color=theme.get_border_color(), border_width=1)
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
        self.func_input.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="ew")
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

        self.solve_button = ctk.CTkButton(self.input_frame, text="Execute Mission", command=self.solve_action)
        self.solve_button.grid(row=9, column=0, padx=20, pady=(20, 10))

        self.smart_solve_button = ctk.CTkButton(
            self.input_frame, 
            text="Smart Solve (Compare)", 
            command=self.smart_solve_action,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.smart_solve_button.grid(row=10, column=0, padx=20, pady=(0, 20))

        # Inline Error Display
        self.error_label = ctk.CTkLabel(self.input_frame, text="", text_color="red", font=ctk.CTkFont(size=11))
        self.error_label.grid(row=11, column=0, padx=20, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=theme.get_panel_color(), border_color=theme.get_border_color(), border_width=1)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        self.viz_frame.grid_rowconfigure(0, weight=1) # Plot takes 1/2
        self.viz_frame.grid_rowconfigure(1, weight=1) # ResultPanel takes 1/2
        self.viz_frame.grid_columnconfigure(0, weight=1)

        # Plot Container
        self.plot_container = ctk.CTkFrame(self.viz_frame, fg_color="transparent")
        self.plot_container.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.plot_container.grid_columnconfigure(0, weight=1)
        self.plot_container.grid_rowconfigure(0, weight=1)

        self.viz_label = ctk.CTkLabel(self.plot_container, text="Function Visualization", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.grid(row=0, column=0, padx=10, pady=(0, 10))

        self.plot_placeholder = ctk.CTkFrame(self.plot_container, fg_color=theme.get_bg_color(), corner_radius=5)
        self.plot_placeholder.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        self.plot_manager = PlotManager(self.plot_placeholder)

        # Result Panel (Methodology Table)
        self.result_panel = ResultPanel(self.viz_frame)
        self.result_panel.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        # Smart Solver Panel (initially hidden)
        self.smart_panel_container = ctk.CTkFrame(self.viz_frame, fg_color="transparent")
        self.smart_panel_container.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.smart_panel_container.grid_forget()  # Hidden by default
        self.smart_panel_container.grid_columnconfigure(0, weight=1)
        self.smart_panel_container.grid_rowconfigure(0, weight=1)
        self.current_smart_panel = None

        # Solvers mapping
        self.solvers = {
            "Trapezoidal Rule": TrapezoidalSolver(),
            "Simpson's 1/3": SimpsonsRuleSolver(),
            "Simpson's 3/8": SimpsonsRuleSolver(),
            "Midpoint Rule": MidpointSolver(),
            "Gaussian Quadrature": GaussianQuadratureSolver(),
            "Differentiation": NumericalDifferentiationSolver()
        }

    def update_theme(self):
        """Update all widget colors when theme changes."""
        self.configure(fg_color=theme.get_bg_color())
        self.input_frame.configure(fg_color=theme.get_panel_color(), border_color=theme.get_border_color())
        self.viz_frame.configure(fg_color=theme.get_panel_color(), border_color=theme.get_border_color())
        self.plot_container.configure(fg_color="transparent")
        self.plot_placeholder.configure(fg_color=theme.get_bg_color())
        # Refresh the plot manager's theme
        if hasattr(self, 'plot_manager') and self.plot_manager:
            self.plot_manager._apply_dark_theme()
            self.plot_manager.canvas.draw()

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
        
        # Show result panel and hide smart panel when doing regular solve
        self.smart_panel_container.grid_forget()
        if self.current_smart_panel:
            self.current_smart_panel.destroy()
            self.current_smart_panel = None
        self.result_panel.grid()
        
        method = self.method_menu.get()
        expression = self.func_input.get_expression()
        
        if not expression:
            self.error_label.configure(text="Error: Expression is required.")
            return

        try:
            import time
            start_time = time.perf_counter()

            f = SymbolicParser.parse_expression(expression)
            solver = self.solvers[method]
            
            if method == "Differentiation":
                x = float(self.range_entry.get())
                h = float(self.n_entry.get())
                data = solver.solve(f=f, x=x, h=h, method="central")
                steps = solver.get_steps()
                
                # Update Result Panel
                self.result_panel.update_result(data, steps)
                
                # Use the new derivative tangent plot
                res = data.metadata.get("derivative")
                self.plot_manager.plot_derivative_tangent(expression, x, res)
                
            elif method == "Gaussian Quadrature":
                r_str = self.range_entry.get()
                a, b = map(float, r_str.split(","))
                pts = int(self.n_entry.get())
                data = solver.solve(f=f, a=a, b=b, points=pts)
                steps = solver.get_steps()
                
                # Update Result Panel
                self.result_panel.update_result(data, steps)
                
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
                steps = solver.get_steps()
                
                # Update Result Panel
                self.result_panel.update_result(data, steps)
                
                # Use the new integration area plot
                self.plot_manager.plot_integration_area(expression, a, b, method)

            end_time = time.perf_counter()
            comp_time = end_time - start_time

            # Update Dashboard status
            if hasattr(self.master.master, "update_status"):
                self.master.master.update_status(f"{method} Solver", comp_time)

        except Exception as e:
            self.error_label.configure(text=f"Error: {str(e)}")

    def smart_solve_action(self):
        """Runs all compatible calculus solvers and shows comparison."""
        self.error_label.configure(text="")
        expression = self.func_input.get_expression()
        method = self.method_menu.get()

        if not expression:
            self.error_label.configure(text="Error: Expression is required.")
            return

        try:
            f = SymbolicParser.parse_expression(expression)
            
            # Filter solvers based on current mode (Integration or Differentiation)
            if method == "Differentiation":
                # Compare differentiation solvers
                diff_solvers = {"Differentiation": self.solvers["Differentiation"]}
                runner = ComparisonRunner(diff_solvers)
                x = float(self.range_entry.get())
                h = float(self.n_entry.get())
                kwargs = {"f": f, "x": x, "h": h, "method": "central"}
            else:
                # Integration solvers
                integration_solvers = {k: v for k, v in self.solvers.items() if k != "Differentiation"}
                runner = ComparisonRunner(integration_solvers)
                r_str = self.range_entry.get()
                a, b = map(float, r_str.split(","))
                n = int(self.n_entry.get())
                kwargs = {"f": f, "a": a, "b": b, "n": n, "points": 3} # Default points for Gaussian
            
            comparison_result = runner.run_comparison(**kwargs)
            
            # Hide result panel and show SmartSolverPanel
            self.result_panel.grid_forget()
            if self.current_smart_panel:
                self.current_smart_panel.destroy()
            self.smart_panel_container.grid()
            self.current_smart_panel = SmartSolverPanel(self.smart_panel_container, comparison_result)
            self.current_smart_panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        except Exception as e:
            self.error_label.configure(text=f"Smart Solve Error: {str(e)}")
