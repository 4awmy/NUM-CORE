import customtkinter as ctk
import numpy as np
from numcore_gui.visualization import PlotManager
from numcore_engine.models import SimulationData
from numcore_engine.solvers.calculus_engine import SimpsonsRuleSolver
from numcore_engine.parser import SymbolicParser

class Chapter4AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Problem & Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Work Done Computation", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Problem Statement
        self.problem_text = (
            "Problem: Computing Work Done by a Variable Force\n\n"
            "The work done W by a force F(x) moving an object from x=a to x=b is "
            "given by the integral of F(x) dx from a to b.\n\n"
            "Example: A spring force F(x) = 50*x + 10*x^2. Find the work done "
            "to compress the spring from x=0 to x=2 meters."
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
        self.func_label = ctk.CTkLabel(self.input_frame, text="Force Function F(x):")
        self.func_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.func_entry = ctk.CTkEntry(self.input_frame)
        self.func_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.func_entry.insert(0, "50*x + 10*x**2")

        self.a_label = ctk.CTkLabel(self.input_frame, text="Start Position (a):")
        self.a_label.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        self.a_entry = ctk.CTkEntry(self.input_frame)
        self.a_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.a_entry.insert(0, "0")

        self.b_label = ctk.CTkLabel(self.input_frame, text="End Position (b):")
        self.b_label.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")
        self.b_entry = ctk.CTkEntry(self.input_frame)
        self.b_entry.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.b_entry.insert(0, "2")

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
        
        self.viz_label = ctk.CTkLabel(self.viz_frame, text="Force vs Distance (Area = Work)", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(self.viz_frame, fg_color="gray20", corner_radius=5)
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.plot_manager = PlotManager(self.plot_placeholder)
        self.solver = SimpsonsRuleSolver()

    def solve_action(self):
        expression = self.func_entry.get()
        a = float(self.a_entry.get())
        b = float(self.b_entry.get())
        
        try:
            f = SymbolicParser.parse_expression(expression)
            data = self.solver.solve(f=f, a=a, b=b, n=100, method="1/3")
            
            self.plot_manager.plot_integration_area(expression, a, b, "Simpson's 1/3")
            
            result = data.metadata.get("total_integral")
            self.result_label.configure(text=f"Total Work Done:\n{result:.4f} Joules")
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")
