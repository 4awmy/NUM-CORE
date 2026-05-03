import customtkinter as ctk
from typing import List
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData, NumericalStep
from numcore_gui.help_system import HelpProvider
from numcore_gui.theme import BLACK, PANEL, BORDER
from numcore_engine.solvers.network_solver import GaussSeidelSolver, JacobiSolver

class NetworkSolverPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BLACK, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Ch 2: Linear Systems", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Help button next to title
        self.help_button = HelpProvider.create_help_button(self.input_frame, "network_solver")
        self.help_button.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        # Method Selection
        self.method_label = ctk.CTkLabel(self.input_frame, text="Select Method:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        self.method_menu = ctk.CTkOptionMenu(
            self.input_frame, 
            values=["Gauss-Seidel", "Jacobi"]
        )
        self.method_menu.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.matrix_size_label = ctk.CTkLabel(self.input_frame, text="Matrix Size (n x n):")
        self.matrix_size_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.matrix_size_optionmenu = ctk.CTkOptionMenu(
            self.input_frame,
            values=["2", "3", "4", "5"],
            command=self._on_matrix_size_change
        )
        self.matrix_size_optionmenu.set("3") # Default size
        self.matrix_size_optionmenu.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Load Examples
        self.load_example_label = ctk.CTkLabel(self.input_frame, text="Load Example:")
        self.load_example_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.load_example_optionmenu = ctk.CTkOptionMenu(
            self.input_frame,
            values=["(a) 3x3", "(b) 3x3", "(c) 4x4", "Custom"],
            command=self._load_example
        )
        self.load_example_optionmenu.set("Custom") # Default to custom
        self.load_example_optionmenu.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Frame for dynamic matrix and vector entries
        self.matrix_input_frame = ctk.CTkScrollableFrame(self.input_frame, label_text="Coefficient Matrix (A) and Constant Vector (b)", fg_color=BLACK)
        self.matrix_input_frame.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.input_frame.grid_rowconfigure(7, weight=1) # Allow matrix input frame to expand

        self.matrix_entries = []
        self.vector_entries = []
        self.current_matrix_size = int(self.matrix_size_optionmenu.get())
        self._create_matrix_input_grid(self.current_matrix_size)

        # Diagonal dominance help button
        self.diag_help_button = HelpProvider.create_help_button(self.input_frame, "diagonal_dominance")
        self.diag_help_button.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")
        
        # Tolerance
        self.tol_label = ctk.CTkLabel(self.input_frame, text="Tolerance:")
        self.tol_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")
        self.tol_entry = ctk.CTkEntry(self.input_frame, placeholder_text="1e-6")
        self.tol_entry.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.tol_entry.insert(0, "1e-6")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Solve System", command=self.solve_action)
        self.solve_button.grid(row=11, column=0, padx=20, pady=20)

        # Results area
        self.results_panel = ctk.CTkFrame(self.input_frame, corner_radius=5, fg_color=BLACK, border_color=BORDER, border_width=1)
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
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        self.viz_frame.grid_rowconfigure(0, weight=6) # 60% for plot
        self.viz_frame.grid_rowconfigure(1, weight=4) # 40% for iteration table
        self.viz_frame.grid_columnconfigure(0, weight=1)

        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Matrix Heatmap / Convergence", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.grid(row=0, column=0, padx=20, pady=(10,0), sticky="n")

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color=BLACK, corner_radius=5)
        self.plot_placeholder.grid(row=0, column=0, padx=20, pady=(40, 10), sticky="nsew")
        
        self.plot_manager = PlotManager(self.plot_placeholder)

        # Iteration Table Frame
        self.iteration_table_frame = ctk.CTkFrame(self.viz_frame, corner_radius=5, fg_color=BLACK)
        self.iteration_table_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.iteration_table_frame.grid_columnconfigure(0, weight=1)
        self.iteration_table_frame.grid_rowconfigure(0, weight=1)

        self.iteration_table_scrollable_frame = ctk.CTkScrollableFrame(self.iteration_table_frame, label_text="Iteration History", fg_color=BLACK)
        self.iteration_table_scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.iteration_table_scrollable_frame.grid_columnconfigure(0, weight=1) # Make first column (Iter) expand


        # Solvers mapping
        self.solvers = {
            "Gauss-Seidel": GaussSeidelSolver(),
            "Jacobi": JacobiSolver()
        }

    _EXAMPLE_PROBLEMS = {
        "(a) 3x3": {
            "size": 3,
            "A": [[3, -1, 1], [3, 6, 2], [3, 3, 7]],
            "b": [1, 0, 4]
        },
        "(b) 3x3": {
            "size": 3,
            "A": [[10, -1, 0], [-1, 10, -2], [0, -2, 10]],
            "b": [9, 7, 6]
        },
        "(c) 4x4": {
            "size": 4,
            "A": [[2, -2, 1, 1], [0, -3, 0.5, 1], [0, 0, 5, -1], [0, 0, 0, 2]],
            "b": [0.8, -6.6, 4.5, 3]
        }
    }

    def _clear_input_grid(self):
        for widget in self.matrix_input_frame.winfo_children():
            widget.destroy()
        self.matrix_entries = []
        self.vector_entries = []

    def _create_matrix_input_grid(self, size):
        self._clear_input_grid()
        self.current_matrix_size = size

        # Labels for Matrix A
        ctk.CTkLabel(self.matrix_input_frame, text="A:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = ctk.CTkEntry(self.matrix_input_frame, width=50)
                entry.grid(row=i, column=j+1, padx=2, pady=2, sticky="ew")
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
            self.matrix_input_frame.grid_columnconfigure(i+1, weight=1) # Configure column weight for expansion

            # Label for Vector b
            # This label is for the entire vector column, placed only once for clarity
            if i == 0: # Place 'b:' label only once
                ctk.CTkLabel(self.matrix_input_frame, text="b:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=size + 1, padx=5, pady=5, sticky="e")
            
            vector_entry = ctk.CTkEntry(self.matrix_input_frame, width=50)
            vector_entry.grid(row=i, column=size + 2, padx=2, pady=2, sticky="ew")
            self.vector_entries.append(vector_entry)
        
        # Configure matrix_input_frame rows to expand
        for i in range(size):
            self.matrix_input_frame.grid_rowconfigure(i, weight=1)
        self.matrix_input_frame.grid_columnconfigure(size + 2, weight=1) # Ensure last column for b-vector expands

    def _on_matrix_size_change(self, new_size_str):
        new_size = int(new_size_str)
        if new_size != self.current_matrix_size:
            self._create_matrix_input_grid(new_size)
            # Clear entries when size changes, and reset example selection
            for row in self.matrix_entries:
                for entry in row:
                    entry.delete(0, ctk.END)
            for entry in self.vector_entries:
                entry.delete(0, ctk.END)
            self.load_example_optionmenu.set("Custom")

    def _load_example(self, problem_key):
        if problem_key == "Custom":
            return

        example_data = self._EXAMPLE_PROBLEMS.get(problem_key)
        if not example_data:
            self.error_label.configure(text=f"Error: Example '{problem_key}' not found.")
            return

        size = example_data["size"]
        A = example_data["A"]
        b = example_data["b"]

        self.matrix_size_optionmenu.set(str(size))
        # Ensure the grid is recreated if the loaded example has a different size
        if size != self.current_matrix_size:
            self._create_matrix_input_grid(size)

        for i in range(size):
            for j in range(size):
                self.matrix_entries[i][j].delete(0, ctk.END)
                self.matrix_entries[i][j].insert(0, str(A[i][j]))
            self.vector_entries[i].delete(0, ctk.END)
            self.vector_entries[i].insert(0, str(b[i]))

    def _display_iteration_table(self, steps: List[NumericalStep]):
        # Clear previous table content
        for widget in self.iteration_table_scrollable_frame.winfo_children():
            widget.destroy()

        if not steps:
            ctk.CTkLabel(self.iteration_table_scrollable_frame, text="No iteration data available.").grid(row=0, column=0, padx=5, pady=5)
            return

        # Headers
        headers = ["Iter"]
        # Determine number of x variables from the first step's details
        first_step_x_values = steps[0].details.get("x_values", [])
        for i in range(len(first_step_x_values)):
            headers.append(f"x{i+1}")
        headers.append("Max Error")

        for col_idx, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(self.iteration_table_scrollable_frame, text=header_text, font=ctk.CTkFont(weight="bold"))
            header_label.grid(row=0, column=col_idx, padx=5, pady=5, sticky="ew")

        # Data rows
        for row_idx, step in enumerate(steps):
            col_offset = 0
            # Iteration number
            ctk.CTkLabel(self.iteration_table_scrollable_frame, text=str(step.step_idx)).grid(row=row_idx + 1, column=col_offset, padx=5, pady=2)
            col_offset += 1

            # x values
            x_values = step.details.get("x_values", [])
            for val in x_values:
                ctk.CTkLabel(self.iteration_table_scrollable_frame, text=f"{val:.4f}").grid(row=row_idx + 1, column=col_offset, padx=5, pady=2)
                col_offset += 1
            
            # Max Error
            error_text = f"{step.error:.4e}" if step.error is not None else "N/A"
            ctk.CTkLabel(self.iteration_table_scrollable_frame, text=error_text).grid(row=row_idx + 1, column=col_offset, padx=5, pady=2)
            
            # Configure column weights for data columns
            for col in range(len(headers)):
                self.iteration_table_scrollable_frame.grid_columnconfigure(col, weight=1)

    def solve_action(self):
        """Triggers the numerical solver and updates the matrix heatmap."""
        self.error_label.configure(text="")
        method = self.method_menu.get()
        
        try:
            # Parse Matrix A
            A = []
            for i in range(self.current_matrix_size):
                row = []
                for j in range(self.current_matrix_size):
                    try:
                        val = float(self.matrix_entries[i][j].get())
                        row.append(val)
                    except ValueError:
                        raise ValueError(f"Invalid input for Matrix A at row {i+1}, column {j+1}. Please enter a number.")
                A.append(row)

            # Parse Vector b
            b = []
            for i in range(self.current_matrix_size):
                try:
                    val = float(self.vector_entries[i].get())
                    b.append(val)
                except ValueError:
                    raise ValueError(f"Invalid input for Vector b at row {i+1}. Please enter a number.")
            
            # Parse Tolerance
            tol = float(self.tol_entry.get() or 1e-6)
            
            solver = self.solvers[method]
            data = solver.solve(A=A, b=b, tol=tol)
            
            # Visualization logic
            steps = solver.get_steps() # Always get steps to populate the table

            # Plotting logic based on matrix size
            if len(A) == 2:
                # For 2x2 systems, show the vector field (lines intersection)
                self.plot_manager.plot_vector_field(A, b)
            else:
                # For larger systems, show the iteration error history
                self.plot_manager.plot_iteration_history(steps)
            
            self._display_iteration_table(steps) # Display iteration table

            # Update results
            x_sol = data.y_data
            iters = data.metadata.get("iterations")
            converged = data.metadata.get("converged", True)
            reordered = data.metadata.get("reordered", False)
            diverged = data.metadata.get("diverged", False)
            
            status = "Success"
            if diverged:
                status = "DIVERGED"
            elif not converged:
                status = "Max Iterations Reached"
            
            reorder_msg = "\n(Matrix was reordered for dominance)" if reordered else ""
            
            sol_str = ", ".join([f"{val:.4f}" for val in x_sol])
            self.result_label.configure(
                text=f"Status: {status}{reorder_msg}\nSolution x: [{sol_str}]\nIterations: {iters}",
                font=ctk.CTkFont(size=11)
            )
            
        except Exception as e:
            self.error_label.configure(text=f"Error: {str(e)}")
