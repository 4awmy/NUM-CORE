import customtkinter as ctk
import numpy as np
import ast
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_engine.solvers.calculus_engine import NewtonDividedDifferenceSolver

class Chapter3AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Problem & Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Thermodynamic Data Fitting", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Problem Statement
        self.problem_text = (
            "Problem: Interpolating Temperature vs Pressure\n\n"
            "An engineer has recorded the pressure of a gas at specific temperatures. "
            "We need to estimate the pressure at a temperature not present in the "
            "recorded data using Newton's Divided Difference Interpolation.\n\n"
            "Data Points (Temp °C, Pressure kPa):\n"
            "(0, 101.3), (20, 108.6), (40, 115.9), (60, 123.2), (80, 130.5)"
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
        self.x_label = ctk.CTkLabel(self.input_frame, text="Temperature Points (X):")
        self.x_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.x_entry = ctk.CTkEntry(self.input_frame)
        self.x_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.x_entry.insert(0, "[0, 20, 40, 60, 80]")

        self.y_label = ctk.CTkLabel(self.input_frame, text="Pressure Points (Y):")
        self.y_label.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        self.y_entry = ctk.CTkEntry(self.input_frame)
        self.y_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.y_entry.insert(0, "[101.3, 108.6, 115.9, 123.2, 130.5]")

        self.target_label = ctk.CTkLabel(self.input_frame, text="Target Temperature:")
        self.target_label.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")
        self.target_entry = ctk.CTkEntry(self.input_frame)
        self.target_entry.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.target_entry.insert(0, "35")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Solve Example", command=self.solve_action)
        self.solve_button.grid(row=8, column=0, padx=20, pady=20)

        # Results area
        self.results_panel = ctk.CTkFrame(self.input_frame, corner_radius=5, fg_color=("gray85", "gray15"))
        self.results_panel.grid(row=9, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)
        
        self.result_title = ctk.CTkLabel(self.results_panel, text="Computation Results", font=ctk.CTkFont(size=12, weight="bold"))
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.result_label = ctk.CTkLabel(self.results_panel, text="Click 'Solve Example' to begin.", font=ctk.CTkFont(size=11))
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Pressure vs Temperature Curve", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)
        self.solver = NewtonDividedDifferenceSolver()

    def solve_action(self):
        try:
            x_points = ast.literal_eval(self.x_entry.get())
            y_points = ast.literal_eval(self.y_entry.get())
            target_x = float(self.target_entry.get())
            
            data = self.solver.solve(x_points=x_points, y_points=y_points, target_x=target_x)
            res_y = data.y_data[0] if isinstance(data.y_data, list) else data.y_data
            
            # Generate smooth curve for plotting
            x_smooth = np.linspace(min(x_points), max(x_points), 100).tolist()
            smooth_data = self.solver.solve(x_points=x_points, y_points=y_points, target_x=x_smooth)
            
            plot_data = SimulationData(
                title="Interpolated Pressure Curve",
                x_data=x_smooth,
                y_data=smooth_data.y_data,
                metadata={"scatter_x": x_points, "scatter_y": y_points}
            )
            self.plot_manager.plot_static(plot_data)
            
            # Manually highlight the target point
            self.plot_manager.ax.scatter([target_x], [res_y], color='red', s=100, zorder=6, label="Target Point")
            self.plot_manager.ax.legend()
            self.plot_manager.canvas.draw()
            
            self.result_label.configure(text=f"Estimated Pressure at {target_x}°C:\n{res_y:.4f} kPa")
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")
