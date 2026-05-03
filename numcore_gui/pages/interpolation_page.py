import customtkinter as ctk
import ast
import numpy as np
import re
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider
from numcore_engine.solvers.calculus_engine import (
    LagrangeInterpolationSolver,
    NewtonDividedDifferenceSolver,
    NewtonDifferenceTableSolver
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
            "Newton Forward Difference": NewtonDifferenceTableSolver()
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
                "Newton Forward Difference"
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

        # X Points
        self.x_label = ctk.CTkLabel(self.input_frame, text="X Points (list):")
        self.x_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.x_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., [0, 1, 2]")
        self.x_entry.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Y Points
        self.y_label = ctk.CTkLabel(self.input_frame, text="Y Points (list):")
        self.y_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.y_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., [1, 3, 2]")
        self.y_entry.grid(row=8, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Target X
        self.target_label = ctk.CTkLabel(self.input_frame, text="Target X (optional):")
        self.target_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")
        self.target_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 1.5")
        self.target_entry.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Solve Interpolation", command=self.solve_action)
        self.solve_button.grid(row=11, column=0, padx=20, pady=20)

        # Results area
        self.results_panel = ctk.CTkFrame(self.input_frame, corner_radius=5, fg_color=("gray85", "gray15"))
        self.results_panel.grid(row=12, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="No data computed yet.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Inline Error Display
        self.error_label = ctk.CTkLabel(self.input_frame, text="", text_color="red", font=ctk.CTkFont(size=11))
        self.error_label.grid(row=13, column=0, padx=20, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        self.viz_frame.grid_rowconfigure(0, weight=1)
        self.viz_frame.grid_rowconfigure(1, weight=1)
        self.viz_frame.grid_columnconfigure(0, weight=1)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.plot_manager = PlotManager(self.plot_placeholder)

        # Difference Table Frame
        self.difference_table_frame = ctk.CTkScrollableFrame(self.viz_frame, label_text="Difference Table", corner_radius=5)
        self.difference_table_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def _load_example_problems_from_md(self) -> list:
        try:
            with open("numerical_methods_problems.md", "r") as f:
                markdown_content = f.read()
            return self._parse_interpolation_problems(markdown_content)
        except FileNotFoundError:
            return []

    def _parse_interpolation_problems(self, markdown_content: str) -> list:
        problems = []
        sheet4_match = re.search(r"### Sheet 4: Chapter 3 - Interpolation and Polynomial Approximation\s*(.*?)(?=\n### Sheet|\Z)", markdown_content, re.DOTALL)
        if not sheet4_match: return problems
        sheet4_content = sheet4_match.group(1)
        lagrange_section_match = re.search(r"I\. Lagrange's Interpolation:\s*(.*?)(?=\n\n|\Z)", sheet4_content, re.DOTALL)
        if not lagrange_section_match: return problems
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
        return problems

    def _load_example_callback(self, choice):
        if choice == "Load Example": return
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
        self.result_label.configure(text="")
        
        for widget in self.difference_table_frame.winfo_children():
            widget.destroy()

        method = self.method_menu.get()
        
        try:
            x_points = ast.literal_eval(self.x_entry.get())
            y_points = ast.literal_eval(self.y_entry.get())
            target_x_str = self.target_entry.get().strip()
            target_x = float(target_x_str) if target_x_str else None

            solver = self.solvers[method]
            data = None
            interpolated_y = None
            
            if method == "Newton Forward Difference":
                data = solver.solve(x_points=x_points, y_points=y_points)
                if target_x_str:
                    self.error_label.configure(text="Warning: Target X not directly used by NFD Table method.")
            else:
                data = solver.solve(x_points=x_points, y_points=y_points, target_x=target_x)
                if target_x is not None and data.y_data:
                    interpolated_y = data.y_data[0]

            if interpolated_y is not None:
                self.result_label.configure(text=f"Interpolated value at x={target_x}: {interpolated_y:.6f}")
            else:
                self.result_label.configure(text="Computation successful.")

            # Display Difference Table
            if method == "Newton Forward Difference" and "difference_table" in data.metadata:
                table_data = np.array(data.metadata["difference_table"])
                ctk.CTkLabel(self.difference_table_frame, text="X", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=2)
                ctk.CTkLabel(self.difference_table_frame, text="Y", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5, pady=2)
                
                max_diff_cols = table_data.shape[1] if len(table_data) > 0 else 0
                for i in range(max_diff_cols - 1):
                    ctk.CTkLabel(self.difference_table_frame, text=f"Δ^{i+1}Y", font=ctk.CTkFont(weight="bold")).grid(row=0, column=i+2, padx=5, pady=2)
                
                for r_idx, row in enumerate(table_data):
                    ctk.CTkLabel(self.difference_table_frame, text=f"{x_points[r_idx]:.4f}").grid(row=r_idx + 1, column=0, padx=5, pady=2)
                    ctk.CTkLabel(self.difference_table_frame, text=f"{row[0]:.6f}").grid(row=r_idx + 1, column=1, padx=5, pady=2)
                    for c_idx, val in enumerate(row[1:]):
                        if not np.isnan(val):
                            ctk.CTkLabel(self.difference_table_frame, text=f"{val:.6f}").grid(row=r_idx + 1, column=c_idx + 2, padx=5, pady=2)

            # Plotting
            points = list(zip(x_points, y_points))
            if method in ["Lagrange Interpolation", "Newton Divided Difference"]:
                plot_solver = self.solvers[method]
                def poly_f(x):
                    res = plot_solver.solve(x_points=x_points, y_points=y_points, target_x=float(x))
                    return res.y_data[0] if res.y_data else 0.0
                self.plot_manager.plot_interpolation_result(points, poly_f)
            else:
                # For NFD, just plot points for now
                plot_data = SimulationData(
                    title="Newton Forward Difference Points",
                    x_data=x_points,
                    y_data=y_points,
                    metadata={"scatter_x": x_points, "scatter_y": y_points}
                )
                self.plot_manager.plot_static(plot_data)

        except Exception as e:
            self.error_label.configure(text=f"Error: {str(e)}")
