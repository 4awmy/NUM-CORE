import ast
import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider
from numcore_engine.solvers.network_solver import GaussSeidelSolver, JacobiSolver


class NetworkSolverPage(ctk.CTkFrame):
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
            self.input_frame, text="Mission: Circuit Analysis",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.help_button = HelpProvider.create_help_button(self.input_frame, "network_solver")
        self.help_button.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")

        # Tab view for the two iterative linear solvers
        self.tabview = ctk.CTkTabview(self.input_frame)
        self.tabview.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # ── Gauss-Seidel tab ────────────────────────────────────────────────
        self.tabview.add("Gauss-Seidel")
        gs_tab = self.tabview.tab("Gauss-Seidel")
        gs_tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            gs_tab,
            text="Solve Ax = b using Gauss-Seidel.\nUpdates each variable immediately.",
            justify="left"
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        gs_matrix_row = ctk.CTkFrame(gs_tab, fg_color="transparent")
        gs_matrix_row.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="ew")
        gs_matrix_row.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(gs_matrix_row, text="Resistance Matrix A (rows as lists):").grid(
            row=0, column=0, sticky="w"
        )
        self.diag_help_button = HelpProvider.create_help_button(
            gs_matrix_row, "diagonal_dominance"
        )
        self.diag_help_button.grid(row=0, column=1, padx=(5, 0), sticky="e")

        self.gs_matrix_entry = ctk.CTkTextbox(gs_tab, height=90)
        self.gs_matrix_entry.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.gs_matrix_entry.insert("0.0", "[[10, -1, 2],\n [-1, 11, -1],\n [2, -1, 10]]")

        ctk.CTkLabel(gs_tab, text="Voltage Vector b:").grid(
            row=3, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.gs_vector_entry = ctk.CTkEntry(gs_tab, placeholder_text="e.g., [6, 25, -11]")
        self.gs_vector_entry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")

        gs_btn_frame = ctk.CTkFrame(gs_tab, fg_color="transparent")
        gs_btn_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        gs_btn_frame.grid_columnconfigure(0, weight=1)
        gs_btn_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            gs_btn_frame, text="Load Example", command=self.load_gs_example
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        ctk.CTkButton(
            gs_btn_frame, text="Analyze Circuit", command=self.solve_gs
        ).grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        self.gs_result_label = ctk.CTkLabel(
            gs_tab, text="Currents will appear here...",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.gs_result_label.grid(row=6, column=0, padx=10, pady=5)

        # ── Jacobi tab ──────────────────────────────────────────────────────
        self.tabview.add("Jacobi")
        jc_tab = self.tabview.tab("Jacobi")
        jc_tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            jc_tab,
            text="Solve Ax = b using Jacobi iteration.\nAll variables updated simultaneously.",
            justify="left"
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(jc_tab, text="Resistance Matrix A (rows as lists):").grid(
            row=1, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.jc_matrix_entry = ctk.CTkTextbox(jc_tab, height=90)
        self.jc_matrix_entry.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.jc_matrix_entry.insert("0.0", "[[10, -1, 2],\n [-1, 11, -1],\n [2, -1, 10]]")

        ctk.CTkLabel(jc_tab, text="Voltage Vector b:").grid(
            row=3, column=0, padx=10, pady=(5, 0), sticky="w"
        )
        self.jc_vector_entry = ctk.CTkEntry(jc_tab, placeholder_text="e.g., [6, 25, -11]")
        self.jc_vector_entry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")

        jc_btn_frame = ctk.CTkFrame(jc_tab, fg_color="transparent")
        jc_btn_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        jc_btn_frame.grid_columnconfigure(0, weight=1)
        jc_btn_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            jc_btn_frame, text="Load Example", command=self.load_jc_example
        ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        ctk.CTkButton(
            jc_btn_frame, text="Analyze Circuit", command=self.solve_jc
        ).grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        self.jc_result_label = ctk.CTkLabel(
            jc_tab, text="Currents will appear here...",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.jc_result_label.grid(row=6, column=0, padx=10, pady=5)

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.viz_label = ctk.CTkLabel(
            self.viz_frame, text="Network Topology / Convergence",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)

        self.plot_manager = PlotManager(self.plot_placeholder)

    # ── Shared helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _parse_matrix(text: str):
        """Parse a 2-D list literal from user text."""
        return ast.literal_eval(text.strip())

    @staticmethod
    def _parse_vector(text: str):
        """Parse a 1-D list literal from user text."""
        return ast.literal_eval(text.strip())

    # ── Load Example helpers ────────────────────────────────────────────────

    def load_gs_example(self):
        """Load default Gauss-Seidel example (3×3 diagonally dominant system)."""
        self.gs_matrix_entry.delete("0.0", "end")
        self.gs_matrix_entry.insert("0.0", "[[10, -1, 2],\n [-1, 11, -1],\n [2, -1, 10]]")
        self.gs_vector_entry.delete(0, "end")
        self.gs_vector_entry.insert(0, "[6, 25, -11]")

    def load_jc_example(self):
        """Load default Jacobi example (same 3×3 diagonally dominant system)."""
        self.jc_matrix_entry.delete("0.0", "end")
        self.jc_matrix_entry.insert("0.0", "[[10, -1, 2],\n [-1, 11, -1],\n [2, -1, 10]]")
        self.jc_vector_entry.delete(0, "end")
        self.jc_vector_entry.insert(0, "[6, 25, -11]")

    # ── Solve actions ───────────────────────────────────────────────────────

    def solve_gs(self):
        """Triggers the Gauss-Seidel solver and updates the heatmap."""
        try:
            A = self._parse_matrix(self.gs_matrix_entry.get("0.0", "end"))
            b = self._parse_vector(self.gs_vector_entry.get().strip())
            solver = GaussSeidelSolver()
            result = solver.solve(A=A, b=b, title="Gauss-Seidel Solution")
            currents = [f"{v:.4f}" for v in result.y_data]
            data = SimulationData(
                title="Resistance Matrix Heatmap",
                x_data=[], y_data=[],
                metadata={"matrix": A}
            )
            self.plot_manager.plot_heatmap(data)
            self.gs_result_label.configure(
                text=f"Circuit Analyzed!\nCurrents: {currents}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
        except Exception as e:
            self.gs_result_label.configure(
                text=f"Error: {e}", font=ctk.CTkFont(size=12)
            )

    def solve_jc(self):
        """Triggers the Jacobi solver and updates the heatmap."""
        try:
            A = self._parse_matrix(self.jc_matrix_entry.get("0.0", "end"))
            b = self._parse_vector(self.jc_vector_entry.get().strip())
            solver = JacobiSolver()
            result = solver.solve(A=A, b=b, title="Jacobi Solution")
            currents = [f"{v:.4f}" for v in result.y_data]
            data = SimulationData(
                title="Resistance Matrix Heatmap",
                x_data=[], y_data=[],
                metadata={"matrix": A}
            )
            self.plot_manager.plot_heatmap(data)
            self.jc_result_label.configure(
                text=f"Circuit Analyzed!\nCurrents: {currents}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
        except Exception as e:
            self.jc_result_label.configure(
                text=f"Error: {e}", font=ctk.CTkFont(size=12)
            )
