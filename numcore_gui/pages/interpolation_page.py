import customtkinter as ctk
import ast
import numpy as np
import re
import textwrap
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider
from numcore_engine.solvers.calculus_engine import (
    LagrangeInterpolationSolver,
    NewtonDividedDifferenceSolver,
    NewtonDifferenceTableSolver,
    LinearInterpolationSolver,
    CubicSplineSolver
)

class InterpolationPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
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
        self.result_label.configure(text="") # Clear previous results
        # Clear and hide difference table
        for widget in self.difference_table_frame.winfo_children():
            widget.destroy()
        self.difference_table_frame.pack_forget()

        method = self.method_menu.get()
        
        try:
            x_points = ast.literal_eval(self.x_entry.get())
            y_points = ast.literal_eval(self.y_entry.get())
            target_x_str = self.target_entry.get().strip()
            target_x = float(target_x_str) if target_x_str else None # Define target_x here for scope

            solver = self.solvers[method]
            data = None
            interpolated_y = None
            
            if method == "Newton Forward Difference":
                # NFD table solver does not take target_x for its primary solve method
                data = solver.solve(x_points=x_points, y_points=y_points)
                if target_x_str: # Warn if target_x was provided, but not used by NFD table solver
                    self.error_label.configure(text="Warning: Target X is not directly computed by Newton Forward Difference Table method. Displaying table only.")
            else: # Lagrange or Newton Divided Difference
                data = solver.solve(x_points=x_points, y_points=y_points, target_x=target_x)
                if target_x is not None:
                    interpolated_y = data.y_data[0] if isinstance(data.y_data, list) else data.y_data
                # else: interpolated_y remains None


            # Update results
            if interpolated_y is not None:
                self.result_label.configure(text=f"Interpolated value at x={target_x}: {interpolated_y:.6f}")
            elif data and (data.y_data is not None) and (len(data.y_data) > 0): 
                 # If solve was successful and returned y_data (e.g., initial points for NFD without target_x)
                 self.result_label.configure(text="Computation successful.")
            else:
                self.result_label.configure(text="No specific interpolated value computed.")

            # Clear previous plot
            self.plot_manager.clear_plot()

            # Display Difference Table for Newton Forward Difference
            if method == "Newton Forward Difference" and "difference_table" in data.metadata:
                self.difference_table_frame.pack(padx=20, pady=(10, 20), fill="both", expand=False)
                table_data = np.array(data.metadata["difference_table"])
                
                for widget in self.difference_table_frame.winfo_children():
                    widget.destroy()

                # Headers for X, Y, and differences
                ctk.CTkLabel(self.difference_table_frame, text="X", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=2, sticky="ew")
                ctk.CTkLabel(self.difference_table_frame, text="Y", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5, pady=2, sticky="ew")
                
                max_diff_cols = 0
                if len(table_data) > 0:
                    max_diff_cols = table_data.shape[1] # Number of columns in the difference table, including y values

                for i in range(max_diff_cols -1): # Column 0 is Y, rest are differences
                    ctk.CTkLabel(self.difference_table_frame, text=f"Δ^{i+1}Y", font=ctk.CTkFont(weight="bold")).grid(row=0, column=i+2, padx=5, pady=2, sticky="ew")
                
                # Populate table with data
                for r_idx, row in enumerate(table_data):
                    # Display X point
                    ctk.CTkLabel(self.difference_table_frame, text=f"{x_points[r_idx]:.4f}").grid(row=r_idx + 1, column=0, padx=5, pady=2, sticky="ew")
                    
                    # Display Y point (first column of the table_data corresponds to Y values)
                    ctk.CTkLabel(self.difference_table_frame, text=f"{row[0]:.6f}").grid(row=r_idx + 1, column=1, padx=5, pady=2, sticky="ew")

                    # Display differences
                    for c_idx, val in enumerate(row[1:]): # Iterate over difference columns
                        if not np.isnan(val):
                            ctk.CTkLabel(self.difference_table_frame, text=f"{val:.6f}").grid(row=r_idx + 1, column=c_idx + 2, padx=5, pady=2, sticky="ew")
            else:
                self.difference_table_frame.pack_forget()
            
            # Plotting logic for interpolation curves
            points = list(zip(x_points, y_points))
            if method in ["Lagrange Interpolation", "Newton Divided Difference", "Linear Interpolation", "Cubic Spline Interpolation"]:
                x_min, x_max = min(x_points), max(x_points)
                x_smooth = np.linspace(x_min, x_max, 100).tolist()
                
                # Plotting requires a solver that can evaluate at arbitrary x values
                plot_solver = self.solvers[method] 
                poly_f = lambda x: plot_solver.solve(x_points=x_points, y_points=y_points, target_x=float(x)).y_data[0]
                self.plot_manager.plot_interpolation_result(points, poly_f)
            else: # For Newton Forward Difference, just plot the original points
                 self.plot_manager.plot_points(points, title="Original Points for Newton Forward Difference")

        except Exception as e:
            self.error_label.configure(text=f"Error: {str(e)}")
