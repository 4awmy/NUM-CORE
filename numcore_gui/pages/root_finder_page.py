import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider

class RootFinderPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Mission: Beam Stress", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Help button next to title
        self.help_button = HelpProvider.create_help_button(self.input_frame, "root_finder")
        self.help_button.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        self.desc_label = ctk.CTkLabel(self.input_frame, text="Calculate optimal beam thickness\nusing Newton-Raphson.", justify="left")
        self.desc_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Placeholder for inputs
        self.func_label = ctk.CTkLabel(self.input_frame, text="Stress Equation f(x):")
        self.func_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.func_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., x**2 - 5")
        self.func_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.guess_label = ctk.CTkLabel(self.input_frame, text="Initial Guess:")
        self.guess_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        self.guess_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 1.0")
        self.guess_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Execute Mission", command=self.solve_action)
        self.solve_button.grid(row=6, column=0, padx=20, pady=20)

        # Results area
        self.results_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.results_frame.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        self.result_label = ctk.CTkLabel(self.results_frame, text="Results will appear here...", font=ctk.CTkFont(size=12, slant="italic"))
        self.result_label.grid(row=0, column=0)

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Trajectory Visualization", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        # Placeholder for Matplotlib plot
        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Initialize PlotManager
        self.plot_manager = PlotManager(self.plot_placeholder)

    def solve_action(self):
        """Triggers the numerical solver and updates the convergence plot."""
        # Mock data for convergence tracking
        data = SimulationData(
            title="Newton-Raphson Convergence",
            x_data=list(range(10)),
            y_data=[2.0, 1.5, 1.2, 1.05, 1.01, 1.001, 1.0, 1.0, 1.0, 1.0]
        )
        self.plot_manager.animate_convergence(data)
        self.result_label.configure(text="Mission Executed!\nRoot found at: 1.0000", font=ctk.CTkFont(size=12, weight="bold"))
