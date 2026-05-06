import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.solvers.root_finder import NewtonRaphsonSolver
from numcore_gui.equation_input import EquationInputWidget
from numcore_gui import theme

class Chapter1AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.get_bg_color(), **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Problem & Inputs
        self.input_frame = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color=theme.get_panel_color(), border_color=theme.get_border_color(), border_width=1)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Beam Stress Analysis", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Problem Statement
        self.problem_text = (
            "Problem: Finding Optimal Beam Thickness\n\n"
            "A structural beam is subjected to a load. The internal stress S as a function "
            "of thickness t is modeled by:\n"
            "S(t) = t^3 - 20t^2 + 100t - 50\n\n"
            "We need to find the thickness t where the stress is exactly zero to identify "
            "the transition point in material behavior."
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
        self.example_label = ctk.CTkLabel(self.input_frame, text="Example Parameters:", font=ctk.CTkFont(weight="bold"))
        self.example_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        self.func_input = EquationInputWidget(
            self.input_frame, 
            label_text="Stress Function S(t):",
            placeholder="e.g., x**3 - 20*x**2 + 100*x - 50"
        )
        self.func_input.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")
        self.func_input.set_expression("x**3 - 20*x**2 + 100*x - 50")

        self.guess_label = ctk.CTkLabel(self.input_frame, text="Initial Guess (t0):")
        self.guess_label.grid(row=5, column=0, padx=20, pady=(5, 0), sticky="w")
        self.guess_entry = ctk.CTkEntry(self.input_frame)
        self.guess_entry.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.guess_entry.insert(0, "1.0")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Solve Example", command=self.solve_action)
        self.solve_button.grid(row=7, column=0, padx=20, pady=20)

        # Results area
        self.results_panel = ctk.CTkFrame(self.input_frame, corner_radius=5, fg_color=theme.get_bg_color(), border_color=theme.get_border_color(), border_width=1)
        self.results_panel.grid(row=8, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="Click 'Solve Example' to begin.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=theme.get_panel_color(), border_color=theme.get_border_color(), border_width=1)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Stress Convergence Plot", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color=theme.get_bg_color(), corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)

        self.solver = NewtonRaphsonSolver()

    def update_theme(self):
        """Update all widget colors when theme changes."""
        self.configure(fg_color=theme.get_bg_color())
        self.input_frame.configure(fg_color=theme.get_panel_color(), border_color=theme.get_border_color())
        self.results_panel.configure(fg_color=theme.get_bg_color(), border_color=theme.get_border_color())
        self.viz_frame.configure(fg_color=theme.get_panel_color(), border_color=theme.get_border_color())
        self.plot_placeholder.configure(fg_color=theme.get_bg_color())
        # Refresh the plot manager's theme
        if hasattr(self, 'plot_manager') and self.plot_manager:
            self.plot_manager._apply_dark_theme()
            self.plot_manager.canvas.draw()

    def solve_action(self):
        expression = self.func_input.get_expression()
        guess = float(self.guess_entry.get())
        
        try:
            import time
            start_time = time.perf_counter()

            data = self.solver.solve(expression=expression, initial_guess=guess, tolerance=1e-6)
            steps = self.solver.get_steps()

            end_time = time.perf_counter()
            comp_time = end_time - start_time

            # Update Dashboard status
            if hasattr(self.master.master, "update_status"):
                self.master.master.update_status("Beam Stress Solver", comp_time)

            iteration_labels = [f"Iter {step.step_idx}" for step in steps]
            error_values = [step.error if step.error is not None else 0.0 for step in steps]
            self.plot_manager.plot_bar(
                iteration_labels,
                error_values,
                title="Stress Convergence Bar Chart",
                xlabel="Iteration",
                ylabel="Absolute Error"
            )
            
            root = data.metadata.get("root")
            iters = data.metadata.get("iterations")
            
            self.result_label.configure(
                text=f"Optimal Thickness found: {root:.4f} units\nIterations required: {iters}"
            )
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")
