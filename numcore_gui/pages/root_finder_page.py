import customtkinter as ctk
import math
from numcore_gui.visualization import PlotManager
from numcore_gui.theme import BLACK, PANEL, BORDER
from numcore_gui.result_panel import ResultPanel

from numcore_gui.help_system import HelpProvider
from numcore_engine.solvers.root_finder import (
    BisectionSolver, 
    NewtonRaphsonSolver, 
    SecantSolver, 
    SimpleIterationSolver
)
from numcore_engine.solvers.comparison import ComparisonRunner
from numcore_gui.smart_solver_panel import SmartSolverPanel

class RootFinderPage(ctk.CTkFrame):
    EXAMPLE_PROBLEMS = {
        "Bisection": [
            {
                "name": "Prob 1a: x^3 - 7x^2 + 14x - 6 on [0, 1]",
                "expression": "x**3 - 7*x**2 + 14*x - 6",
                "a": "0",
                "b": "1",
                "tol": "1e-2"
            },
            {
                "name": "Prob 1b: x^3 - 7x^2 + 14x - 6 on [1, 3.2]",
                "expression": "x**3 - 7*x**2 + 14*x - 6",
                "a": "1",
                "b": "3.2",
                "tol": "1e-2"
            },
            {
                "name": "Prob 1c: x^3 - 7x**2 + 14x - 6 on [3.2, 4]",
                "expression": "x**3 - 7*x**2 + 14*x - 6",
                "a": "3.2",
                "b": "4",
                "tol": "1e-2"
            },
            {
                "name": "Prob 2: x - tan(x) on [4, 4.5]",
                "expression": "x - math.tan(x)",
                "a": "4",
                "b": "4.5",
                "tol": "1e-3"
            },
            {
                "name": "Prob 3: e^x - x^2 + 3x - 2 on [0, 1]",
                "expression": "math.exp(x) - x**2 + 3*x - 2",
                "a": "0",
                "b": "1",
                "tol": "1e-5"
            },
        ],
        "Secant": [
            {
                "name": "Prob 1a: x^3 - 2x^2 - 5 on [1, 4]",
                "expression": "x**3 - 2*x**2 - 5",
                "x0": "1",
                "x1": "4",
                "tol": "1e-4"
            },
            {
                "name": "Prob 1b: x - cos(x) on [0, pi/2]",
                "expression": "x - math.cos(x)",
                "x0": "0",
                "x1": str(math.pi / 2),
                "tol": "1e-4"
            },
            {
                "name": "Prob 2: ln(x-1) + cos(x-1) on [1.3, 2]",
                "expression": "math.log(x-1) + math.cos(x-1)",
                "x0": "1.3",
                "x1": "2",
                "tol": "1e-4"
            },
        ],
        "Simple Iteration": [
            {
                "name": "Prob 1: 0.5x - sin(x) = 0, g(x) = 2sin(x), x0=pi/2",
                "expression": "2 * math.sin(x)",
                "x0": str(math.pi / 2),
                "tol": "1e-5"
            },
            {
                "name": "Prob 2: x^3 - 7x + 1 = 0, g(x)=(x^3+1)/7, x0=0",
                "expression": "(x**3 + 1)/7",
                "x0": "0",
                "tol": "1e-3"
            },
            {
                "name": "Prob 3: x - cos(x) = 0, g(x)=cos(x), x0=pi/2",
                "expression": "math.cos(x)",
                "x0": str(math.pi / 2),
                "tol": "1e-3"
            },
        ],
        "Newton-Raphson": [
            {
                "name": "Prob 1a: x^3 - 2x^2 - 5 = 0 on [1, 4], x0=1",
                "expression": "x**3 - 2*x**2 - 5",
                "x0": "1",
                "tol": "1e-4"
            },
            {
                "name": "Prob 1b: x - 0.8 - 0.2sin(x) = 0 on [0, pi/2], x0=0",
                "expression": "x - 0.8 - 0.2 * math.sin(x)",
                "x0": "0",
                "tol": "1e-4"
            },
        ],
    }
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BLACK, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel: Inputs
        self.input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.input_frame, text="Ch 1: Root Finding", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Help button next to title
        self.help_button = HelpProvider.create_help_button(self.input_frame, "root_finder")
        self.help_button.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        # Method Selection
        self.method_label = ctk.CTkLabel(self.input_frame, text="Select Method:")
        self.method_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        self.method_menu = ctk.CTkOptionMenu(
            self.input_frame, 
            values=["Newton-Raphson", "Bisection", "Secant", "Simple Iteration"],
            command=self.update_inputs
        )
        self.method_menu.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.example_menu_label = ctk.CTkLabel(self.input_frame, text="Load Example:")
        self.example_menu_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.example_menu = ctk.CTkOptionMenu(
            self.input_frame,
            values=["No Examples Available"],
            command=self.load_example
        )
        self.example_menu.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Visualization Type Selection
        self.viz_type_label = ctk.CTkLabel(self.input_frame, text="Visualization Type:")
        self.viz_type_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.viz_type_menu = ctk.CTkOptionMenu(
            self.input_frame,
            values=["Solution Path", "Convergence Error"]
        )
        self.viz_type_menu.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Input Fields
        self.func_label = ctk.CTkLabel(self.input_frame, text="Equation f(x):")
        self.func_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        self.func_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., x**2 - 5")
        self.func_entry.grid(row=8, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Dynamic Input 1 (Guess / a / x0)
        self.input1_label = ctk.CTkLabel(self.input_frame, text="Initial Guess:")
        self.input1_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")
        self.input1_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 1.0")
        self.input1_entry.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Dynamic Input 2 (b / x1) - Hidden by default
        self.input2_label = ctk.CTkLabel(self.input_frame, text="Upper Bound (b):")
        self.input2_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 3.0")
        
        # Tolerance and Max Iterations
        self.tol_label = ctk.CTkLabel(self.input_frame, text="Tolerance:")
        self.tol_label.grid(row=13, column=0, padx=20, pady=(10, 0), sticky="w")
        self.tol_entry = ctk.CTkEntry(self.input_frame, placeholder_text="1e-6")
        self.tol_entry.grid(row=14, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.tol_entry.insert(0, "1e-6")

        self.solve_button = ctk.CTkButton(self.input_frame, text="Solve Equation", command=self.solve_action)
        self.solve_button.grid(row=15, column=0, padx=20, pady=(20, 10))

        self.smart_solve_button = ctk.CTkButton(
            self.input_frame, 
            text="Smart Solve (Compare)", 
            command=self.smart_solve_action,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.smart_solve_button.grid(row=16, column=0, padx=20, pady=(0, 20))

        # Inline Error Display
        self.error_label = ctk.CTkLabel(self.input_frame, text="", text_color="red", font=ctk.CTkFont(size=11))
        self.error_label.grid(row=17, column=0, padx=20, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        self.viz_frame.grid_rowconfigure(0, weight=1) # Plot takes 1/2
        self.viz_frame.grid_rowconfigure(1, weight=1) # ResultPanel takes 1/2
        self.viz_frame.grid_columnconfigure(0, weight=1)

        # Plot Container
        self.plot_container = ctk.CTkFrame(self.viz_frame, fg_color="transparent")
        self.plot_container.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.plot_container.grid_columnconfigure(0, weight=1)
        self.plot_container.grid_rowconfigure(0, weight=1)

        self.viz_label = ctk.CTkLabel(self.plot_container, text="Convergence Trajectory", font=ctk.CTkFont(size=16, weight="bold"))
        self.viz_label.grid(row=0, column=0, padx=10, pady=(0, 10)) # Adjust padding

        # Placeholder for Matplotlib plot
        self.plot_placeholder = ctk.CTkFrame(self.plot_container, fg_color=BLACK, corner_radius=5)
        self.plot_placeholder.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew") # Adjusted grid
        
        # Initialize PlotManager
        self.plot_manager = PlotManager(self.plot_placeholder)

        # Result Panel (Methodology Table)
        self.result_panel = ResultPanel(self.viz_frame)
        self.result_panel.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        # Solvers mapping
        self.solvers = {
            "Newton-Raphson": NewtonRaphsonSolver(),
            "Bisection": BisectionSolver(),
            "Secant": SecantSolver(),
            "Simple Iteration": SimpleIterationSolver()
        }

        self.update_inputs("Newton-Raphson")

    def load_example(self, example_name):
        """Loads the selected example problem into the input fields."""
        method = self.method_menu.get()
        examples_for_method = self.EXAMPLE_PROBLEMS.get(method, [])
        
        selected_example = next((ex for ex in examples_for_method if ex["name"] == example_name), None)

        if selected_example:
            self.func_entry.delete(0, ctk.END)
            self.func_entry.insert(0, selected_example.get("expression", ""))
            
            self.tol_entry.delete(0, ctk.END)
            self.tol_entry.insert(0, selected_example.get("tol", "1e-6"))

            self.input1_entry.delete(0, ctk.END)
            self.input2_entry.delete(0, ctk.END)

            if method == "Bisection":
                self.input1_entry.insert(0, selected_example.get("a", ""))
                self.input2_entry.insert(0, selected_example.get("b", ""))
            elif method == "Secant":
                self.input1_entry.insert(0, selected_example.get("x0", ""))
                self.input2_entry.insert(0, selected_example.get("x1", ""))
            elif method == "Newton-Raphson" or method == "Simple Iteration":
                self.input1_entry.insert(0, selected_example.get("x0", ""))
        else:
            self.error_label.configure(text=f"Error: Example '{example_name}' not found for method '{method}'.")

    def update_inputs(self, method):
        """Updates the input fields based on the selected method."""
        # Reset labels and grid visibility
        if method == "Bisection":
            self.input1_label.configure(text="Lower Bound (a):")
            self.input2_label.configure(text="Upper Bound (b):")
            self.input2_label.grid(row=11, column=0, padx=20, pady=(10, 0), sticky="w")
            self.input2_entry.grid(row=12, column=0, padx=20, pady=(0, 10), sticky="ew")
        elif method == "Secant":
            self.input1_label.configure(text="First Guess (x0):")
            self.input2_label.configure(text="Second Guess (x1):")
            self.input2_label.grid(row=11, column=0, padx=20, pady=(10, 0), sticky="w")
            self.input2_entry.grid(row=12, column=0, padx=20, pady=(0, 10), sticky="ew")
        elif method == "Newton-Raphson":
            self.input1_label.configure(text="Initial Guess (x0):")
            self.input2_label.grid_forget()
            self.input2_entry.grid_forget()
            self.func_label.configure(text="Equation f(x):")
        elif method == "Simple Iteration":
            self.input1_label.configure(text="Initial Guess (x0):")
            self.input2_label.grid_forget()
            self.input2_entry.grid_forget()
            self.func_label.configure(text="Iteration Function g(x):")
        
        if method != "Simple Iteration":
            self.func_label.configure(text="Equation f(x):")

        # Update examples menu
        examples = self.EXAMPLE_PROBLEMS.get(method, [])
        if examples:
            self.example_menu.configure(values=[ex["name"] for ex in examples])
            self.example_menu.set(examples[0]["name"])
        else:
            self.example_menu.configure(values=["No Examples Available"])
            self.example_menu.set("No Examples Available")

    def solve_action(self):
        """Triggers the root finder solver and updates visualization."""
        self.error_label.configure(text="")
        method = self.method_menu.get()
        expression = self.func_entry.get()

        if not expression:
            self.error_label.configure(text="Error: Expression is required.")
            return

        try:
            tol = float(self.tol_entry.get() or 1e-6)
            solver = self.solvers[method]

            kwargs = {
                "expression": expression,
                "tolerance": tol,
                "max_iterations": 100
            }

            if method == "Bisection":
                kwargs["a"] = float(self.input1_entry.get())
                kwargs["b"] = float(self.input2_entry.get())
            elif method == "Secant":
                kwargs["x0"] = float(self.input1_entry.get())
                kwargs["x1"] = float(self.input2_entry.get())
            elif method == "Newton-Raphson" or method == "Simple Iteration":
                kwargs["initial_guess"] = float(self.input1_entry.get())

            data = solver.solve(**kwargs)
            steps = solver.get_steps()

            # Update Result Panel (Methodology Table)
            self.result_panel.update_result(data, steps)

            # Visualization
            viz_type = self.viz_type_menu.get()
            if viz_type == "Solution Path":
                self.plot_manager.plot_solution_path(steps, expression if method != "Simple Iteration" else None)
            else:
                self.plot_manager.plot_iteration_history(steps)

        except Exception as e:
            self.error_label.configure(text=f"Error: {str(e)}")

    def smart_solve_action(self):
        """Runs all compatible root finders and shows comparison."""
        self.error_label.configure(text="")
        expression = self.func_entry.get()

        if not expression:
            self.error_label.configure(text="Error: Expression is required.")
            return

        try:
            tol = float(self.tol_entry.get() or 1e-6)
            runner = ComparisonRunner(self.solvers)

            kwargs = {
                "expression": expression,
                "tolerance": tol,
                "max_iterations": 100
            }

            # Try to gather all possible inputs
            try: kwargs["a"] = float(self.input1_entry.get())
            except: pass
            try: kwargs["b"] = float(self.input2_entry.get())
            except: pass
            try: kwargs["x0"] = float(self.input1_entry.get())
            except: pass
            try: kwargs["x1"] = float(self.input2_entry.get())
            except: pass
            try: kwargs["initial_guess"] = float(self.input1_entry.get())
            except: pass

            comparison_result = runner.run_comparison(**kwargs)

            # Show SmartSolverPanel
            SmartSolverPanel(self, comparison_result)

        except Exception as e:
            self.error_label.configure(text=f"Smart Solve Error: {str(e)}")