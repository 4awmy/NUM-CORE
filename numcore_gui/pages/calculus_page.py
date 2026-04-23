import ast
import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider
from numcore_engine.solvers.calculus_engine import IntegrationSolver, InterpolationSolver


class CalculusPage(ctk.CTkFrame):
    """
    Calculus engine page for numerical integration and interpolation.
    """

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
            self.input_frame, text="Mission: Calculus Engine",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.help_button = HelpProvider.create_help_button(self.input_frame, "calculus")
        self.help_button.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")

        # Tab view for the two calculus methods
        self.tabview = ctk.CTkTabview(self.input_frame)
        self.tabview.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # ── Integration tab ─────────────────────────────────────────────────
        self.tabview.add("Integration")
        integ_tab = self.tabview.tab("Integration")
        integ_tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            integ_tab,
            text="Numerical Integration (Trapezoidal / Simpson's).\nProvide equally-spaced x and y data points.",
            justify="left"
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(integ_tab, text="X points (comma-separated):").grid(
            row=1, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.integ_x_entry = ctk.CTkEntry(integ_tab, placeholder_text="e.g., 0, 0.5, 1.0, 1.5, 2.0")
        self.integ_x_entry.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")

        ctk.CTkLabel(integ_tab, text="Y points (comma-separated):").grid(
            row=3, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.integ_y_entry = ctk.CTkEntry(integ_tab, placeholder_text="e.g., 0, 0.47, 0.84, 0.99, 0.91")
        self.integ_y_entry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")

        ctk.CTkLabel(integ_tab, text="Method:").grid(
            row=5, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.integ_method_menu = ctk.CTkOptionMenu(
            integ_tab, values=["trapezoidal", "simpson13", "simpson38"]
        )
        self.integ_method_menu.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.integ_method_menu.set("trapezoidal")

        integ_btn_frame = ctk.CTkFrame(integ_tab, fg_color="transparent")
        integ_btn_frame.grid(row=7, column=0, padx=10, pady=10, sticky="ew")
        integ_btn_frame.grid_columnconfigure(0, weight=1)
        integ_btn_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            integ_btn_frame, text="Load Example", command=self.load_integ_example
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        ctk.CTkButton(
            integ_btn_frame, text="Execute Mission", command=self.solve_integ
        ).grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        self.integ_result_label = ctk.CTkLabel(
            integ_tab, text="Results will appear here...",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.integ_result_label.grid(row=8, column=0, padx=10, pady=5)

        # ── Interpolation tab ───────────────────────────────────────────────
        self.tabview.add("Interpolation")
        interp_tab = self.tabview.tab("Interpolation")
        interp_tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            interp_tab,
            text="Newton's Divided Difference Interpolation.\nEstimate f(x) from known data points.",
            justify="left"
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(interp_tab, text="X points (comma-separated):").grid(
            row=1, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.interp_x_entry = ctk.CTkEntry(interp_tab, placeholder_text="e.g., 1, 2, 3, 4")
        self.interp_x_entry.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")

        ctk.CTkLabel(interp_tab, text="Y points (comma-separated):").grid(
            row=3, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.interp_y_entry = ctk.CTkEntry(interp_tab, placeholder_text="e.g., 1, 4, 9, 16")
        self.interp_y_entry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")

        ctk.CTkLabel(interp_tab, text="Target X (to interpolate):").grid(
            row=5, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.interp_target_entry = ctk.CTkEntry(interp_tab, placeholder_text="e.g., 2.5")
        self.interp_target_entry.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="ew")

        interp_btn_frame = ctk.CTkFrame(interp_tab, fg_color="transparent")
        interp_btn_frame.grid(row=7, column=0, padx=10, pady=10, sticky="ew")
        interp_btn_frame.grid_columnconfigure(0, weight=1)
        interp_btn_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            interp_btn_frame, text="Load Example", command=self.load_interp_example
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        ctk.CTkButton(
            interp_btn_frame, text="Execute Mission", command=self.solve_interp
        ).grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        self.interp_result_label = ctk.CTkLabel(
            interp_tab, text="Results will appear here...",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.interp_result_label.grid(row=8, column=0, padx=10, pady=5)

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.viz_label = ctk.CTkLabel(
            self.viz_frame, text="Function Visualization",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)

        self.plot_manager = PlotManager(self.plot_placeholder)

    # ── Load Example helpers ────────────────────────────────────────────────

    def load_integ_example(self):
        """Load default Integration example: sin(x) sampled over [0, π] (trapezoidal)."""
        self.integ_x_entry.delete(0, "end")
        self.integ_x_entry.insert(0, "0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.14159")
        self.integ_y_entry.delete(0, "end")
        self.integ_y_entry.insert(0, "0, 0.4794, 0.8415, 0.9975, 0.9093, 0.5985, 0.0")
        self.integ_method_menu.set("trapezoidal")

    def load_interp_example(self):
        """Load default Interpolation example: f(x) = x² at integer points, target x = 2.5."""
        self.interp_x_entry.delete(0, "end")
        self.interp_x_entry.insert(0, "1, 2, 3, 4")
        self.interp_y_entry.delete(0, "end")
        self.interp_y_entry.insert(0, "1, 4, 9, 16")
        self.interp_target_entry.delete(0, "end")
        self.interp_target_entry.insert(0, "2.5")

    # ── Shared parse helper ─────────────────────────────────────────────────

    @staticmethod
    def _parse_floats(text: str):
        """Parse a comma-separated list of floats."""
        return [float(v.strip()) for v in text.split(",")]

    # ── Solve actions ───────────────────────────────────────────────────────

    def solve_integ(self):
        """Triggers the Integration solver and updates the static plot."""
        try:
            x_points = self._parse_floats(self.integ_x_entry.get())
            y_points = self._parse_floats(self.integ_y_entry.get())
            method = self.integ_method_menu.get()
            solver = IntegrationSolver()
            result = solver.solve(x_points=x_points, y_points=y_points, method=method)
            total = result.metadata.get("total_integral", "N/A")
            plot_data = SimulationData(
                title=f"Numerical Integration ({method})",
                x_data=x_points, y_data=y_points
            )
            self.plot_manager.plot_static(plot_data)
            self.integ_result_label.configure(
                text=f"Mission Executed!\nIntegral \u2248 {total:.6f}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
        except Exception as e:
            self.integ_result_label.configure(
                text=f"Error: {e}", font=ctk.CTkFont(size=12)
            )

    def solve_interp(self):
        """Triggers the Interpolation solver and updates the static plot."""
        try:
            x_points = self._parse_floats(self.interp_x_entry.get())
            y_points = self._parse_floats(self.interp_y_entry.get())
            target_x_text = self.interp_target_entry.get().strip()
            target_x = float(target_x_text) if target_x_text else None
            solver = InterpolationSolver()
            result = solver.solve(x_points=x_points, y_points=y_points, target_x=target_x)
            self.plot_manager.plot_static(result)
            if target_x is not None and result.y_data:
                interp_val = result.y_data[0]
                self.interp_result_label.configure(
                    text=f"Mission Executed!\nf({target_x}) \u2248 {interp_val:.6f}",
                    font=ctk.CTkFont(size=12, weight="bold")
                )
            else:
                self.interp_result_label.configure(
                    text="Mission Executed!\nInterpolation complete.",
                    font=ctk.CTkFont(size=12, weight="bold")
                )
        except Exception as e:
            self.interp_result_label.configure(
                text=f"Error: {e}", font=ctk.CTkFont(size=12)
            )
