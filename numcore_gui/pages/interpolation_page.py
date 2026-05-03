import customtkinter as ctk
import ast
import numpy as np
import re
from numcore_gui.visualization import PlotManager
from numcore_gui.theme import BLACK, PANEL, BORDER
from numcore_gui.result_panel import ResultPanel
from numcore_gui.help_system import HelpProvider
from numcore_engine.solvers.calculus_engine import (
    LagrangeInterpolationSolver,
    NewtonDividedDifferenceSolver,
    NewtonDifferenceTableSolver,
    LinearInterpolationSolver,
    CubicSplineSolver
)
from numcore_engine.solvers.comparison import ComparisonRunner
from numcore_gui.smart_solver_panel import SmartSolverPanel

class InterpolationPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BLACK, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Solvers mapping
        self.solvers = {
            "Lagrange Interpolation": LagrangeInterpolationSolver(),
            "Newton Divided Difference": NewtonDividedDifferenceSolver(),
            "Newton Forward Difference": NewtonDifferenceTableSolver(),
            "Linear Interpolation": LinearInterpolationSolver(),
            "Cubic Spline Interpolation": CubicSplineSolver()
        }

        self.example_problems = self._load_example_problems_from_md()

        # Left Panel: Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        self.title_label = ctk.CTkLabel(self.input_frame, text="Ch 4: Interpolation", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Help button next to title
        self.help_button = HelpProvider.create_help_button(self.input_frame, "interpolation")
        self.help_button.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        # Method Selection
        self.method_label = ctk.CTkLabel(self.input_frame, text="Select Method:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        self.method_menu = ctk.CTkOptionMenu(
            self.input_frame, 
            values=[
                "Lagrange Interpolation", 
                "Newton Divided Difference", 
                "Newton Forward Difference",
                "Linear Interpolation",
                "Cubic Spline Interpolation"
            ]
        )
        self.method_menu.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Load Examples Dropdown
        self.load_examples_label = ctk.CTkLabel(self.input_frame, text="Load Example:")
        self.load_examples_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.example_options = ["Load Example"] + [p["name"] for p in self.example_problems]
        self.load_examples_menu = ctk.CTkOptionMenu(
            self.input_frame,
            values=self.example_options,
            command=self._load_example_callback
        )
        self.load_examples_menu.set("Load Example")
        self.load_examples_menu.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Input Fields
        self.x_label = ctk.CTkLabel(self.input_frame, text="X Points (list):")
        self.x_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.x_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., [1, 2, 3]")
        self.x_entry.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.y_label = ctk.CTkLabel(self.input_frame, text="Y Points (list):")
        self.y_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.y_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., [0.5, 2.1, 4.2]")
        self.y_entry.grid(row=8, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.target_label = ctk.CTkLabel(self.input_frame, text="Target X (optional):")
        self.target_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")
        self.target_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 1.5")
        self.target_entry.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Interpolate", command=self.solve_action)
        self.solve_button.grid(row=11, column=0, padx=20, pady=(20, 10))

        self.smart_solve_button = ctk.CTkButton(
            self.input_frame, 
            text="Smart Solve (Compare)", 
            command=self.smart_solve_action,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.smart_solve_button.grid(row=12, column=0, padx=20, pady=(0, 20))

        # Inline Error Display
        self.error_label = ctk.CTkLabel(self.input_frame, text="", text_color="red", font=ctk.CTkFont(size=11))
        self.error_label.grid(row=13, column=0, padx=20, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        self.viz_frame.grid_rowconfigure(0, weight=1)
        self.viz_frame.grid_rowconfigure(1, weight=1)
        self.viz_frame.grid_columnconfigure(0, weight=1)
        
        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color=BLACK, corner_radius=5)
        self.plot_placeholder.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.plot_manager = PlotManager(self.plot_placeholder)

        # Result Panel (Methodology Table)
        self.result_panel = ResultPanel(self.viz_frame)
        self.result_panel.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

    def _load_example_problems_from_md(self) -> list:
        try:
            with open("numerical_methods_problems.md", "r") as f:
                markdown_content = f.read()
            return self._parse_interpolation_problems(markdown_content)
        except FileNotFoundError:
            print("Error: numerical_methods_problems.md not found.")
            return []

    def _parse_interpolation_problems(self, markdown_content: str) -> list:
        problems = []
        
        sheet4_match = re.search(r"### Sheet 4: Chapter 3 - Interpolation and Polynomial Approximation\s*(.*?)(?=\n### Sheet|\Z)", markdown_content, re.DOTALL)
        if not sheet4_match:
            return problems

        sheet4_content = sheet4_match.group(1)

        lagrange_section_match = re.search(r"I\. Lagrange's Interpolation:\s*(.*?)(?=\n\n|\Z)", sheet4_content, re.DOTALL)
        if not lagrange_section_match:
            return problems
        
        lagrange_content = lagrange_section_match.group(1)

        # Problem (a)
        problem_a_match = re.search(r"\(a\)\s*f\(1\)=0.1924, f\(1.05\)=0.2414, f\(1.1\)=0.2933, f\(1.15\)=0.3492\. Then find the approximate value of f\(1.09\)", lagrange_content)
        if problem_a_match:
            problems.append({
                "name": "Lagrange Problem (a)",
                "x_points": [1.0, 1.05, 1.1, 1.15],
                "y_points": [0.1924, 0.2414, 0.2933, 0.3492],
                "target_x": 1.09
            })

        # Problem (b)
        problem_b_match = re.search(r"\(b\)\s*f\(0.698\)=0.7661, f\(0.768\)=0.7193, f\(0.733\)=0.7432, f\(0.803\)=0.6946\. Find the approximate value of f\(0.750\)", lagrange_content)
        if problem_b_match:
            problems.append({
                "name": "Lagrange Problem (b)",
                "x_points": [0.698, 0.768, 0.733, 0.803],
                "y_points": [0.7661, 0.7193, 0.7432, 0.6946],
                "target_x": 0.750
            })
        
        return problems

    def _load_example_callback(self, choice):
        if choice == "Load Example": # Default option, do nothing
            return

        selected_problem = next((p for p in self.example_problems if p["name"] == choice), None)
        if selected_problem:
            self.x_entry.delete(0, ctk.END)
            self.x_entry.insert(0, str(selected_problem["x_points"]))
            self.y_entry.delete(0, ctk.END)
            self.y_entry.insert(0, str(selected_problem["y_points"]))
            self.target_entry.delete(0, ctk.END)
            self.target_entry.insert(0, str(selected_problem["target_x"]))

    def solve_action(self):
        """Triggers the numerical interpolation solver and updates the plot."""
        self.error_label.configure(text="")
        self.result_panel.clear()

        method = self.method_menu.get()
        
        try:
            x_points = ast.literal_eval(self.x_entry.get())
            y_points = ast.literal_eval(self.y_entry.get())
            target_x_str = self.target_entry.get().strip()
            target_x = float(target_x_str) if target_x_str else None

            solver = self.solvers[method]
            data = None
            
            if method == "Newton Forward Difference":
                data = solver.solve(x_points=x_points, y_points=y_points)
                if target_x_str:
                    self.error_label.configure(text="Warning: Target X is not directly computed by Newton Forward Difference Table method. Displaying table only.")
            else:
                data = solver.solve(x_points=x_points, y_points=y_points, target_x=target_x)

            steps = solver.get_steps()
            self.result_panel.update_result(data, steps)

            # Clear previous plot
            self.plot_manager.ax.clear()

            # Plotting logic for interpolation curves
            points = list(zip(x_points, y_points))
            if method in ["Lagrange Interpolation", "Newton Divided Difference", "Linear Interpolation", "Cubic Spline Interpolation"]:
                # Plotting requires a solver that can evaluate at arbitrary x values
                plot_solver = self.solvers[method] 
                poly_f = lambda x: plot_solver.solve(x_points=x_points, y_points=y_points, target_x=float(x)).y_data[0]
                self.plot_manager.plot_interpolation_result(points, poly_f, target_x=target_x)
            else: # For Newton Forward Difference, just plot the original points
                 self.plot_manager.ax.scatter(x_points, y_points, color='#ff7f0e', s=50, zorder=5, label="Data Points")
                 self.plot_manager.ax.set_title("Original Points for Newton Forward Difference")
                 self.plot_manager.ax.legend()
                 self.plot_manager.canvas.draw()

        except Exception as e:
            self.error_label.configure(text=f"Error: {str(e)}")

    def smart_solve_action(self):
        """Runs all compatible interpolation solvers and shows comparison."""
        self.error_label.configure(text="")
        try:
            x_points = ast.literal_eval(self.x_entry.get())
            y_points = ast.literal_eval(self.y_entry.get())
            target_x_str = self.target_entry.get().strip()
            target_x = float(target_x_str) if target_x_str else None

            # Filter out Newton Forward Difference if target_x is provided as it doesn't support it directly in solve()
            solvers_to_compare = self.solvers.copy()
            if target_x is not None:
                if "Newton Forward Difference" in solvers_to_compare:
                    del solvers_to_compare["Newton Forward Difference"]

            runner = ComparisonRunner(solvers_to_compare)
            kwargs = {"x_points": x_points, "y_points": y_points, "target_x": target_x}
            
            comparison_result = runner.run_comparison(**kwargs)
            
            # Show SmartSolverPanel
            SmartSolverPanel(self, comparison_result)

        except Exception as e:
            self.error_label.configure(text=f"Smart Solve Error: {str(e)}")
