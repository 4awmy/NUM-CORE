import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.solvers.network_solver import NetworkSolver
from numcore_gui.theme import BLACK, PANEL, BORDER

class Chapter2AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BLACK, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Problem & Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Circuit Analysis", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Problem Statement
        self.problem_text = (
            "Problem: Kirchhoff's Laws in a DC Circuit\n\n"
            "Consider a circuit with 3 loops. Using Kirchhoff's Voltage Law (KVL), "
            "we derive a system of linear equations Ax = B, where x represents the "
            "unknown currents (I1, I2, I3).\n\n"
            "Example System:\n"
            "10*I1 - 2*I2 - 3*I3 = 12\n"
            "-2*I1 + 8*I2 - 1*I3 = 0\n"
            "-3*I1 - 1*I2 + 6*I3 = -5"
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
        self.matrix_label = ctk.CTkLabel(self.input_frame, text="Resistance Matrix (A):")
        self.matrix_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.matrix_entry = ctk.CTkTextbox(self.input_frame, height=80)
        self.matrix_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.matrix_entry.insert("1.0", "10, -2, -3\n-2, 8, -1\n-3, -1, 6")

        self.vector_label = ctk.CTkLabel(self.input_frame, text="Voltage Vector (B):")
        self.vector_label.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        self.vector_entry = ctk.CTkEntry(self.input_frame)
        self.vector_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.vector_entry.insert(0, "12, 0, -5")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Solve", command=self.solve_action)
        self.solve_button.grid(row=6, column=0, padx=20, pady=20)

        # Results area
        self.results_panel = ctk.CTkFrame(self.input_frame, corner_radius=5, fg_color=BLACK, border_color=BORDER, border_width=1)
        self.results_panel.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="Click 'Solve' to begin.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Current Distribution", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color=BLACK, corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)

        self.solver = NetworkSolver()

    def solve_action(self):
        matrix_str = self.matrix_entry.get("1.0", "end-1c")
        vector_str = self.vector_entry.get()
        
        try:
            import time
            start_time = time.perf_counter()

            # Parse matrix
            matrix = [[float(x) for x in row.split(",")] for row in matrix_str.split("\n") if row.strip()]
            # Parse vector
            vector = [float(x) for x in vector_str.split(",")]
            
            data = self.solver.solve(matrix=matrix, vector=vector)
            
            end_time = time.perf_counter()
            comp_time = end_time - start_time

            # Update Dashboard status
            if hasattr(self.master.master, "update_status"):
                self.master.master.update_status("Circuit Analysis Solver", comp_time)

            solution = data.metadata.get("solution")
            
            # Use plot_bar for solution vector
            labels = [f"I{i+1}" for i in range(len(solution))]
            self.plot_manager.plot_bar(
                x=labels, 
                y=solution, 
                title="Branch Current Distribution",
                xlabel="Current Branch",
                ylabel="Current (A)"
            )
            
            sol_text = "\n".join([f"I{i+1} = {val:.4f} A" for i, val in enumerate(solution)])
            
            self.result_label.configure(text=f"Branch Currents:\n{sol_text}")
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")
