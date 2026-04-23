import customtkinter as ctk
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_gui.help_system import HelpProvider

class CalculusPage(ctk.CTkFrame):
    """
    Calculus engine page for numerical integration and differentiation.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Mission: Calculus Engine", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Help button next to title
        self.help_button = HelpProvider.create_help_button(self.input_frame, "calculus")
        self.help_button.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        self.desc_label = ctk.CTkLabel(self.input_frame, text="Numerical Integration & Differentiation\nusing Simpson's and Finite Difference.", justify="left")
        self.desc_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Inputs
        self.func_label = ctk.CTkLabel(self.input_frame, text="Equation f(x):")
        self.func_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.func_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., sin(x)")
        self.func_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.range_label = ctk.CTkLabel(self.input_frame, text="Range [a, b]:")
        self.range_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        self.range_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 0, 3.14")
        self.range_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

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
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Function Visualization", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Initialize PlotManager
        self.plot_manager = PlotManager(self.plot_placeholder)

    def solve_action(self):
        """Triggers the numerical calculus solver and updates the plot."""
        # Mock data for demonstration (Integration area)
        # In a real scenario, this would call the calculus engine
        data = SimulationData(
            title="Numerical Integration Area",
            x_data=[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.14],
            y_data=[0, 0.47, 0.84, 0.99, 0.90, 0.59, 0]
        )
        self.plot_manager.plot_static(data)
        self.result_label.configure(text="Mission Executed!\nIntegral: [Placeholder]", font=ctk.CTkFont(size=12, weight="bold"))
