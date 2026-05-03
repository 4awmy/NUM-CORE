import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.solvers.network_solver import GaussSeidelSolver, JacobiSolver
from numcore_engine.models import SimulationData
from numcore_gui.smart_solver_panel import SmartSolverPanel

class Chapter2AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Problem & Inputs
        self.input_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Chapter 2 Application: Linear Systems", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Problem Statement
        self.problem_text = (
            "Application: Solving Systems of Linear Equations\n\n"
            "Iterative methods like Gauss-Seidel and Jacobi are used to solve large "
            "systems of linear equations Ax = B. These methods are particularly "
            "useful when the matrix A is sparse or diagonally dominant.\n\n"
            "Example System:\n"
            "10*x1 - 2*x2 - 3*x3 = 12\n"
            "-2*x1 + 8*x2 - 1*x3 = 0\n"
            "-3*x1 - 1*x2 + 6*x3 = -5"
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
        self.matrix_label = ctk.CTkLabel(self.input_frame, text="Coefficient Matrix (A):")
        self.matrix_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.matrix_entry = ctk.CTkTextbox(self.input_frame, height=80)
        self.matrix_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.matrix_entry.insert("1.0", "10, -2, -3\n-2, 8, -1\n-3, -1, 6")

        self.vector_label = ctk.CTkLabel(self.input_frame, text="Constant Vector (B):")
        self.vector_label.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        self.vector_entry = ctk.CTkEntry(self.input_frame)
        self.vector_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.vector_entry.insert(0, "12, 0, -5")

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.button_frame.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
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
        self.results_panel.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="Click 'Solve' to begin.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Smart Solver Panel (Inline)
        self.smart_panel = SmartSolverPanel(self.input_frame)
        self.smart_panel.grid(row=8, column=0, padx=20, pady=10, sticky="nsew")
        self.smart_panel.grid_forget() # Hidden by default

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Solution Distribution", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)
        
        self.solvers = {
            "Gauss-Seidel": GaussSeidelSolver(),
            "Jacobi": JacobiSolver()
        }

    def solve_action(self):
        self.smart_panel.grid_forget()
        matrix_str = self.matrix_entry.get("1.0", "end-1c")
        vector_str = self.vector_entry.get()
        
        try:
            # Parse matrix
            matrix = [[float(x) for x in row.split(",")] for row in matrix_str.split("\n") if row.strip()]
            # Parse vector
            vector = [float(x) for x in vector_str.split(",")]
            
            solver = self.solvers["Gauss-Seidel"]
            data = solver.solve(matrix=matrix, vector=vector)
            
            solution = data.metadata.get("solution")
            
            # Create plot data
            plot_data = SimulationData(
                title="Solution Distribution",
                x_data=list(range(1, len(solution) + 1)),
                y_data=solution,
                metadata={"scatter_x": list(range(1, len(solution) + 1)), "scatter_y": solution}
            )
            self.plot_manager.plot_static(plot_data)
            self.plot_manager.ax.set_xlabel("Variable Index")
            self.plot_manager.ax.set_ylabel("Value")
            self.plot_manager.canvas.draw()
            
            sol_text = "\n".join([f"x{i+1} = {val:.4f}" for i, val in enumerate(solution)])
            self.result_label.configure(text=f"Solution:\n{sol_text}")
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")

    def smart_solve_action(self):
        """Compares Gauss-Seidel and Jacobi methods."""
        matrix_str = self.matrix_entry.get("1.0", "end-1c")
        vector_str = self.vector_entry.get()
        
        results = []
        
        try:
            matrix = [[float(x) for x in row.split(",")] for row in matrix_str.split("\n") if row.strip()]
            vector = [float(x) for x in vector_str.split(",")]

            for method_name, solver in self.solvers.items():
                try:
                    data = solver.solve(matrix=matrix, vector=vector, tolerance=1e-6, max_iterations=100)
                    results.append({
                        "method": method_name,
                        "diverged": data.metadata.get("diverged", False),
                        "iterations": data.metadata.get("iterations"),
                        "error": solver.get_steps()[-1].error if solver.get_steps() else 1.0,
                        "root": data.metadata.get("solution"),
                        "reason": "Converged successfully." if not data.metadata.get("diverged") else "Method diverged."
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

            self.smart_panel.grid(row=8, column=0, padx=20, pady=10, sticky="nsew")
            self.smart_panel.populate(results)
            
            converged = [r for r in results if not r['diverged']]
            if converged:
                self.solve_action()
            
        except Exception as e:
            self.result_label.configure(text=f"Smart Solve Error: {str(e)}")

