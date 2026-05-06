import customtkinter as ctk
import time
from numcore_gui.visualization import PlotManager
from numcore_engine.solvers.ode_solvers import EulerSolver, RungeKuttaSolver
from numcore_engine.models import SimulationData
from numcore_gui import theme


class Chapter5AppPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.get_bg_color(), **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel
        self.input_frame = ctk.CTkScrollableFrame(
            self, corner_radius=10,
            fg_color=theme.get_panel_color(),
            border_color=theme.get_border_color(), border_width=1
        )
        self.input_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.input_frame, text="Population Growth (ODE)",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        problem_text = (
            "Problem: Modelling Bacterial Population Growth\n\n"
            "The rate of change of a bacterial population P is governed by:\n"
            "  dP/dt = r * P\n\n"
            "where r is the growth rate. This is equivalent to dy/dx = r * y.\n\n"
            "Starting with P₀ bacteria at t=0, estimate the population over time "
            "using Euler's method and compare with Runge-Kutta 4th order."
        )
        self.problem_label = ctk.CTkLabel(
            self.input_frame, text=problem_text,
            justify="left", wraplength=350, font=ctk.CTkFont(size=12)
        )
        self.problem_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        # Expression input
        self.expr_label = ctk.CTkLabel(self.input_frame, text="ODE  dy/dx = f(x, y):")
        self.expr_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.expr_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. 0.5 * y")
        self.expr_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.expr_entry.insert(0, "0.5 * y")

        # x0 / y0
        self.x0_label = ctk.CTkLabel(self.input_frame, text="Initial x (x₀):")
        self.x0_label.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")
        self.x0_entry = ctk.CTkEntry(self.input_frame)
        self.x0_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.x0_entry.insert(0, "0")

        self.y0_label = ctk.CTkLabel(self.input_frame, text="Initial y (y₀ = P₀):")
        self.y0_label.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")
        self.y0_entry = ctk.CTkEntry(self.input_frame)
        self.y0_entry.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.y0_entry.insert(0, "100")

        # Step size / steps
        self.h_label = ctk.CTkLabel(self.input_frame, text="Step Size (h):")
        self.h_label.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")
        self.h_entry = ctk.CTkEntry(self.input_frame)
        self.h_entry.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.h_entry.insert(0, "0.5")

        self.steps_label = ctk.CTkLabel(self.input_frame, text="Number of Steps:")
        self.steps_label.grid(row=10, column=0, padx=20, pady=(5, 0), sticky="w")
        self.steps_entry = ctk.CTkEntry(self.input_frame)
        self.steps_entry.grid(row=11, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.steps_entry.insert(0, "10")

        # Method selector
        self.method_label = ctk.CTkLabel(self.input_frame, text="Method:")
        self.method_label.grid(row=12, column=0, padx=20, pady=(5, 0), sticky="w")
        self.method_menu = ctk.CTkOptionMenu(
            self.input_frame,
            values=["Euler", "Runge-Kutta 4", "Compare Both"]
        )
        self.method_menu.set("Compare Both")
        self.method_menu.grid(row=13, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Load Example
        self.example_label = ctk.CTkLabel(self.input_frame, text="Load Example:")
        self.example_label.grid(row=14, column=0, padx=20, pady=(10, 0), sticky="w")
        self.example_menu = ctk.CTkOptionMenu(
            self.input_frame,
            values=["Population Growth", "Radioactive Decay", "Logistic Growth", "Cooling Law"],
            command=self.load_example
        )
        self.example_menu.set("Population Growth")
        self.example_menu.grid(row=15, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.solve_button = ctk.CTkButton(
            self.input_frame, text="Solve", command=self.solve_action
        )
        self.solve_button.grid(row=16, column=0, padx=20, pady=20)

        # Results area
        self.results_panel = ctk.CTkFrame(
            self.input_frame, corner_radius=5,
            fg_color=theme.get_bg_color(),
            border_color=theme.get_border_color(), border_width=1
        )
        self.results_panel.grid(row=17, column=0, padx=20, pady=10, sticky="nsew")
        self.results_panel.grid_columnconfigure(0, weight=1)

        self.result_title = ctk.CTkLabel(
            self.results_panel, text="Computation Results",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.result_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        self.result_label = ctk.CTkLabel(
            self.results_panel, text="Click 'Solve' to begin.",
            font=ctk.CTkFont(size=11), justify="left", wraplength=320
        )
        self.result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Right Panel: Visualization
        self.viz_frame = ctk.CTkFrame(
            self, corner_radius=10,
            fg_color=theme.get_panel_color(),
            border_color=theme.get_border_color(), border_width=1
        )
        self.viz_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.viz_label = ctk.CTkLabel(
            self.viz_frame, text="ODE Solution Trajectory",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.viz_label.pack(pady=20)

        self.plot_placeholder = ctk.CTkFrame(
            self.viz_frame, fg_color=theme.get_bg_color(), corner_radius=5
        )
        self.plot_placeholder.pack(padx=20, pady=20, fill="both", expand=True)

        self.plot_manager = PlotManager(self.plot_placeholder)

        self.examples = {
            "Population Growth":  {"expr": "0.5 * y",  "x0": "0", "y0": "100",  "h": "0.5",  "steps": "10"},
            "Radioactive Decay":  {"expr": "-0.3 * y", "x0": "0", "y0": "200",  "h": "1.0",  "steps": "10"},
            "Logistic Growth":    {"expr": "0.4 * y * (1 - y / 500)", "x0": "0", "y0": "50", "h": "0.5", "steps": "20"},
            "Cooling Law":        {"expr": "-0.1 * (y - 20)", "x0": "0", "y0": "80", "h": "1.0", "steps": "15"},
        }

    def load_example(self, name):
        ex = self.examples.get(name, {})
        if not ex:
            return
        self.expr_entry.delete(0, ctk.END)
        self.expr_entry.insert(0, ex["expr"])
        self.x0_entry.delete(0, ctk.END)
        self.x0_entry.insert(0, ex["x0"])
        self.y0_entry.delete(0, ctk.END)
        self.y0_entry.insert(0, ex["y0"])
        self.h_entry.delete(0, ctk.END)
        self.h_entry.insert(0, ex["h"])
        self.steps_entry.delete(0, ctk.END)
        self.steps_entry.insert(0, ex["steps"])

    def update_theme(self):
        self.configure(fg_color=theme.get_bg_color())
        self.input_frame.configure(fg_color=theme.get_panel_color(), border_color=theme.get_border_color())
        self.results_panel.configure(fg_color=theme.get_bg_color(), border_color=theme.get_border_color())
        self.viz_frame.configure(fg_color=theme.get_panel_color(), border_color=theme.get_border_color())
        self.plot_placeholder.configure(fg_color=theme.get_bg_color())
        if hasattr(self, "plot_manager") and self.plot_manager:
            self.plot_manager._apply_dark_theme()
            self.plot_manager.canvas.draw()

    def solve_action(self):
        try:
            expression = self.expr_entry.get().strip()
            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
            h = float(self.h_entry.get())
            steps = int(self.steps_entry.get())
            method = self.method_menu.get()

            params = dict(expression=expression, x0=x0, y0=y0, h=h, steps=steps)

            start = time.perf_counter()

            if method == "Euler":
                data = EulerSolver().solve(**params)
                self._plot_single(data, "Euler")
                final_y = data.y_data[-1]
                msg = f"Euler's Method\nFinal y at x={x0 + h*steps:.2f}: {final_y:.4f}"
            elif method == "Runge-Kutta 4":
                data = RungeKuttaSolver().solve(**params)
                self._plot_single(data, "RK4")
                final_y = data.y_data[-1]
                msg = f"Runge-Kutta 4\nFinal y at x={x0 + h*steps:.2f}: {final_y:.4f}"
            else:  # Compare Both
                euler_data = EulerSolver().solve(**params)
                rk4_data = RungeKuttaSolver().solve(**params)
                self._plot_comparison(euler_data, rk4_data)
                ey = euler_data.y_data[-1]
                ry = rk4_data.y_data[-1]
                diff = abs(ry - ey)
                msg = (
                    f"At x = {x0 + h*steps:.2f}:\n"
                    f"  Euler:  {ey:.4f}\n"
                    f"  RK4:    {ry:.4f}\n"
                    f"  |diff|: {diff:.6f}"
                )

            elapsed = time.perf_counter() - start
            if hasattr(self.master.master, "update_status"):
                self.master.master.update_status(f"ODE ({method})", elapsed)

            self.result_label.configure(text=msg)

        except Exception as e:
            self.result_label.configure(text=f"Error: {e}")

    def _plot_single(self, data: SimulationData, label: str):
        self.plot_manager.ax.clear()
        self.plot_manager._apply_dark_theme()
        self.plot_manager.ax.plot(
            data.x_data, data.y_data,
            color=theme.ACCENT_BLUE, linewidth=2, label=label, marker="o", markersize=4
        )
        self.plot_manager.ax.set_title(f"ODE Solution — {label}")
        self.plot_manager.ax.set_xlabel("x")
        self.plot_manager.ax.set_ylabel("y")
        self.plot_manager.ax.legend()
        self.plot_manager.canvas.draw()

    def _plot_comparison(self, euler_data: SimulationData, rk4_data: SimulationData):
        self.plot_manager.ax.clear()
        self.plot_manager._apply_dark_theme()
        self.plot_manager.ax.plot(
            euler_data.x_data, euler_data.y_data,
            color=theme.ACCENT_BLUE, linewidth=2, label="Euler", marker="o", markersize=4, linestyle="--"
        )
        self.plot_manager.ax.plot(
            rk4_data.x_data, rk4_data.y_data,
            color=theme.ACCENT_ORANGE, linewidth=2, label="RK4", marker="s", markersize=4
        )
        self.plot_manager.ax.set_title("ODE Solution — Euler vs RK4")
        self.plot_manager.ax.set_xlabel("x")
        self.plot_manager.ax.set_ylabel("y")
        self.plot_manager.ax.legend()
        self.plot_manager.canvas.draw()
