import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider
from numcore_engine.solvers.root_finder import NewtonRaphsonSolver, SimpleIterationSolver


class RootFinderPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)

        # Title row
        self.title_label = ctk.CTkLabel(
            self.input_frame, text="Mission: Beam Stress",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.help_button = HelpProvider.create_help_button(self.input_frame, "root_finder")
        self.help_button.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")

        # Tab view for the two root-finding methods
        self.tabview = ctk.CTkTabview(self.input_frame)
        self.tabview.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # ── Newton-Raphson tab ──────────────────────────────────────────────
        self.tabview.add("Newton-Raphson")
        nr_tab = self.tabview.tab("Newton-Raphson")
        nr_tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            nr_tab,
            text="Find roots using Newton-Raphson.\nFormula: x₁ = x₀ - f(x₀) / f'(x₀)",
            justify="left"
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(nr_tab, text="Stress Equation f(x):").grid(
            row=1, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.nr_func_entry = ctk.CTkEntry(nr_tab, placeholder_text="e.g., x**3 - x - 2")
        self.nr_func_entry.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")

        ctk.CTkLabel(nr_tab, text="Initial Guess:").grid(
            row=3, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.nr_guess_entry = ctk.CTkEntry(nr_tab, placeholder_text="e.g., 1.5")
        self.nr_guess_entry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")

        nr_btn_frame = ctk.CTkFrame(nr_tab, fg_color="transparent")
        nr_btn_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        nr_btn_frame.grid_columnconfigure(0, weight=1)
        nr_btn_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            nr_btn_frame, text="Load Example", command=self.load_nr_example
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        ctk.CTkButton(
            nr_btn_frame, text="Execute Mission", command=self.solve_nr
        ).grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        self.nr_result_label = ctk.CTkLabel(
            nr_tab, text="Results will appear here...",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.nr_result_label.grid(row=6, column=0, padx=10, pady=5)

        # ── Simple Iteration tab ────────────────────────────────────────────
        self.tabview.add("Simple Iteration")
        si_tab = self.tabview.tab("Simple Iteration")
        si_tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            si_tab,
            text="Find roots via Fixed-Point iteration.\nFormula: x₁ = g(x₀)",
            justify="left"
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(si_tab, text="Iteration Function g(x):").grid(
            row=1, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.si_func_entry = ctk.CTkEntry(si_tab, placeholder_text="e.g., (x + 2)**(1/3)")
        self.si_func_entry.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")

        ctk.CTkLabel(si_tab, text="Initial Guess:").grid(
            row=3, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.si_guess_entry = ctk.CTkEntry(si_tab, placeholder_text="e.g., 1.5")
        self.si_guess_entry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")

        si_btn_frame = ctk.CTkFrame(si_tab, fg_color="transparent")
        si_btn_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        si_btn_frame.grid_columnconfigure(0, weight=1)
        si_btn_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            si_btn_frame, text="Load Example", command=self.load_si_example
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        ctk.CTkButton(
            si_btn_frame, text="Execute Mission", command=self.solve_si
        ).grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        self.si_result_label = ctk.CTkLabel(
            si_tab, text="Results will appear here...",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.si_result_label.grid(row=6, column=0, padx=10, pady=5)

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.viz_label = ctk.CTkLabel(
            self.viz_frame, text="Trajectory Visualization",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)

        self.plot_manager = PlotManager(self.plot_placeholder)

    # ── Load Example helpers ────────────────────────────────────────────────

    def load_nr_example(self):
        """Load default Newton-Raphson example: f(x) = x³ - x - 2, x₀ = 1.5."""
        self.nr_func_entry.delete(0, "end")
        self.nr_func_entry.insert(0, "x**3 - x - 2")
        self.nr_guess_entry.delete(0, "end")
        self.nr_guess_entry.insert(0, "1.5")

    def load_si_example(self):
        """Load default Simple Iteration example: g(x) = (x + 2)**(1/3), x₀ = 1.5."""
        self.si_func_entry.delete(0, "end")
        self.si_func_entry.insert(0, "(x + 2)**(1/3)")
        self.si_guess_entry.delete(0, "end")
        self.si_guess_entry.insert(0, "1.5")

    # ── Solve actions ───────────────────────────────────────────────────────

    def solve_nr(self):
        """Triggers the Newton-Raphson solver and updates the convergence plot."""
        try:
            expression = self.nr_func_entry.get().strip()
            initial_guess = float(self.nr_guess_entry.get().strip())
            solver = NewtonRaphsonSolver()
            result = solver.solve(expression=expression, initial_guess=initial_guess)
            root = result.metadata.get("root", "N/A")
            iterations = result.metadata.get("iterations", "N/A")
            self.plot_manager.animate_convergence(result)
            self.nr_result_label.configure(
                text=f"Mission Executed!\nRoot \u2248 {root:.6f}\nIterations: {iterations}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
        except Exception as e:
            self.nr_result_label.configure(
                text=f"Error: {e}", font=ctk.CTkFont(size=12)
            )

    def solve_si(self):
        """Triggers the Simple Iteration solver and updates the convergence plot."""
        try:
            expression = self.si_func_entry.get().strip()
            initial_guess = float(self.si_guess_entry.get().strip())
            solver = SimpleIterationSolver()
            result = solver.solve(expression=expression, initial_guess=initial_guess)
            root = result.metadata.get("root", "N/A")
            iterations = result.metadata.get("iterations", "N/A")
            self.plot_manager.animate_convergence(result)
            self.si_result_label.configure(
                text=f"Mission Executed!\nRoot \u2248 {root:.6f}\nIterations: {iterations}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
        except Exception as e:
            self.si_result_label.configure(
                text=f"Error: {e}", font=ctk.CTkFont(size=12)
            )
