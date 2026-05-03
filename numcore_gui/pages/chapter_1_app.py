import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.solvers.root_finder import (
    NewtonRaphsonSolver, 
    BisectionSolver, 
    SecantSolver, 
    SimpleIterationSolver
)
from numcore_gui.equation_input import EquationInputWidget
from numcore_gui.smart_solver_panel import SmartSolverPanel

class Chapter1AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Problem & Inputs
        self.input_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Chapter 1 Application: Root Finding", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Problem Statement
        self.problem_text = (
            "Application: Finding Roots of Nonlinear Equations\n\n"
            "Numerical root-finding methods are essential for solving equations where "
            "analytical solutions are difficult or impossible to obtain. This application "
            "demonstrates how different methods converge to a solution for a given "
            "mathematical model.\n\n"
            "Example Equation:\n"
            "f(x) = x^3 - 20x^2 + 100x - 50"
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
        self.example_label = ctk.CTkLabel(self.input_frame, text="Parameters:", font=ctk.CTkFont(weight="bold"))
        self.example_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        self.func_input = EquationInputWidget(
            self.input_frame, 
            label_text="Function f(x):",
            placeholder="e.g., x**3 - 20*x**2 + 100*x - 50"
        )
        self.func_input.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")
        self.func_input.set_expression("x**3 - 20*x**2 + 100*x - 50")

        self.guess_label = ctk.CTkLabel(self.input_frame, text="Initial Guess (x0):")
        self.guess_label.grid(row=5, column=0, padx=20, pady=(5, 0), sticky="w")
        self.guess_entry = ctk.CTkEntry(self.input_frame)
        self.guess_entry.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.guess_entry.insert(0, "1.0")

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.button_frame.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
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
        self.results_panel.grid(row=8, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="Click 'Solve' to begin.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Smart Solver Panel (Inline)
        self.smart_panel = SmartSolverPanel(self.input_frame)
        self.smart_panel.grid(row=9, column=0, padx=20, pady=10, sticky="nsew")
        self.smart_panel.grid_forget() # Hidden by default

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Convergence Plot", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)
        
        self.solvers = {
            "Newton-Raphson": NewtonRaphsonSolver(),
            "Bisection": BisectionSolver(),
            "Secant": SecantSolver(),
            "Simple Iteration": SimpleIterationSolver()
        }

    def solve_action(self):
        self.smart_panel.grid_forget()
        if not self.func_input.is_valid():
            return

        expression = self.func_input.get_expression()
        guess = float(self.guess_entry.get())
        
        try:
            # Default to Newton-Raphson for the single solve
            solver = self.solvers["Newton-Raphson"]
            data = solver.solve(expression=expression, initial_guess=guess, tolerance=1e-6)
            steps = solver.get_steps()
            self.plot_manager.plot_solution_path(steps, expression)
            
            root = data.metadata.get("root")
            iters = data.metadata.get("iterations")
            
            self.result_label.configure(
                text=f"Root found: {root:.4f}\nIterations required: {iters}"
            )
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")

    def smart_solve_action(self):
        """Compares all available root finding methods."""
        if not self.func_input.is_valid():
            return

        expression = self.func_input.get_expression()
        
        results = []
        
        try:
            x0 = float(self.guess_entry.get())
            x1 = x0 + 1.0

            comparison_configs = [
                ("Newton-Raphson", {"initial_guess": x0}),
                ("Simple Iteration", {"initial_guess": x0}),
                ("Bisection", {"a": x0, "b": x1}),
                ("Secant", {"x0": x0, "x1": x1})
            ]

            for method_name, extra_kwargs in comparison_configs:
                solver = self.solvers[method_name]
                kwargs = {
                    "expression": expression,
                    "tolerance": 1e-6,
                    "max_iterations": 100
                }
                kwargs.update(extra_kwargs)
                
                try:
                    data = solver.solve(**kwargs)
                    results.append({
                        "method": method_name,
                        "diverged": data.metadata.get("diverged", False),
                        "iterations": data.metadata.get("iterations"),
                        "error": solver.get_steps()[-1].error if solver.get_steps() else 1.0,
                        "root": data.metadata.get("root"),
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

            self.smart_panel.grid(row=9, column=0, padx=20, pady=10, sticky="nsew")
            self.smart_panel.populate(results)
            
            # If any converged, plot the best one
            converged = [r for r in results if not r['diverged']]
            if converged:
                best = min(converged, key=lambda x: x['iterations'])
                # Re-run best for plotting
                self.solve_action()
            
        except Exception as e:
            self.result_label.configure(text=f"Smart Solve Error: {str(e)}")

