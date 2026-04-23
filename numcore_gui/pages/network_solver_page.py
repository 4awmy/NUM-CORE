import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider

class NetworkSolverPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Mission: Circuit Analysis", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Help button next to title
        self.help_button = HelpProvider.create_help_button(self.input_frame, "network_solver")
        self.help_button.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        self.desc_label = ctk.CTkLabel(self.input_frame, text="Solve for currents in a circuit\nusing Gauss-Seidel.", justify="left")
        self.desc_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Placeholder for inputs (Matrix A and Vector b)
        self.matrix_label = ctk.CTkLabel(self.input_frame, text="Resistance Matrix (A):")
        self.matrix_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        # Diagonal dominance help
        self.diag_help_button = HelpProvider.create_help_button(self.input_frame, "diagonal_dominance")
        self.diag_help_button.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="e")

        self.matrix_entry = ctk.CTkTextbox(self.input_frame, height=100)
        self.matrix_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.matrix_entry.insert("0.0", "[[10, -1, 2],\n [-1, 11, -1],\n [2, -1, 10]]")

        self.vector_label = ctk.CTkLabel(self.input_frame, text="Voltage Vector (b):")
        self.vector_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        self.vector_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., [6, 25, -11]")
        self.vector_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Analyze Circuit", command=self.solve_action)
        self.solve_button.grid(row=6, column=0, padx=20, pady=20)

        # Results area
        self.results_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.results_frame.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        self.result_label = ctk.CTkLabel(self.results_frame, text="Currents will appear here...", font=ctk.CTkFont(size=12, slant="italic"))
        self.result_label.grid(row=0, column=0)

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Network Topology / Convergence", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        # Placeholder for Matplotlib plot
        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Initialize PlotManager
        self.plot_manager = PlotManager(self.plot_placeholder)

    def solve_action(self):
        """Triggers the numerical solver and updates the matrix heatmap."""
        # Mock data for matrix heatmap
        matrix_data = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]
        data = SimulationData(
            title="Resistance Matrix Heatmap",
            x_data=[],
            y_data=[],
            metadata={"matrix": matrix_data}
        )
        self.plot_manager.plot_heatmap(data)
        self.result_label.configure(text="Circuit Analyzed!\nCurrents: [1.0, 2.0, -1.0]", font=ctk.CTkFont(size=12, weight="bold"))
