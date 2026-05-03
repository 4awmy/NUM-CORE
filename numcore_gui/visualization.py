import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import customtkinter as ctk
import numpy as np
import os
from typing import List, Any, Callable, Optional
from numcore_engine.models import SimulationData, NumericalStep
from numcore_engine.parser import SymbolicParser
from numcore_gui.theme import BLACK, PANEL, BORDER, TEXT_PRIMARY, ACCENT_BLUE, ACCENT_ORANGE

class PlotManager:
    """
    Handles Matplotlib canvas embedding in CustomTkinter.
    Supports interactive plots, dynamic animations, and static exports.
    """
    def __init__(self, master: ctk.CTkFrame):
        self.master = master
        # Clear any existing widgets in the master frame (e.g., placeholders)
        for widget in self.master.winfo_children():
            widget.destroy()

        # Load custom style if available
        style_path = os.path.join(os.path.dirname(__file__), "styles", "numcore_black.mplstyle")
        if os.path.exists(style_path):
            plt.style.use(style_path)
        
        # Create Figure and Axes
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self._apply_dark_theme()

        # Embed in Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Add Navigation Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side="bottom", fill="x")
        self._style_toolbar()

    def _apply_dark_theme(self):
        """Applies a dark theme to the matplotlib figure to match CustomTkinter."""
        self.figure.patch.set_facecolor(BLACK)
        self.ax.set_facecolor(BLACK)
        self.ax.tick_params(colors='white', which='both')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor(BORDER)
        self.ax.grid(True, linestyle='--', alpha=0.2, color=BORDER)

    def _style_toolbar(self):
        """Attempts to style the standard Tkinter toolbar to match the dark theme."""
        self.toolbar.config(background=PANEL)
        for child in self.toolbar.winfo_children():
            try:
                child.config(background=PANEL, foreground='white')
            except:
                pass

    def clear(self):
        """Clears the current plot."""
        self.ax.clear()
        self._apply_dark_theme()
        self.canvas.draw()

    def plot_static(self, data: SimulationData):
        """Renders a static plot from SimulationData."""
        self.ax.clear()
        self._apply_dark_theme()
        
        self.ax.plot(data.x_data, data.y_data, color=ACCENT_BLUE, linewidth=2, label="Function")
        
        # Plot scatter points if provided in metadata
        scatter_x = data.metadata.get("scatter_x")
        scatter_y = data.metadata.get("scatter_y")
        if scatter_x is not None and scatter_y is not None:
            self.ax.scatter(scatter_x, scatter_y, color=ACCENT_ORANGE, s=50, zorder=5, label="Data Points")
            self.ax.legend()

        self.ax.set_title(data.title)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.canvas.draw()

    def plot_bar(self, x: List[Any], y: List[float], title: str, xlabel: str, ylabel: str):
        """Renders a bar chart, useful for solution vectors."""
        self.ax.clear()
        self._apply_dark_theme()
        
        bars = self.ax.bar(x, y, color=ACCENT_BLUE, alpha=0.7, edgecolor='white', linewidth=0.5)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', color='white', fontsize=8)

        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.canvas.draw()

    def animate_convergence(self, data: SimulationData):
        """Creates a 'live' animation of convergence tracking."""
        self.ax.clear()
        self._apply_dark_theme()
        
        line, = self.ax.plot([], [], color=ACCENT_BLUE, linewidth=2, marker='o')
        self.ax.set_title(data.title)
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Value")

        def init():
            line.set_data([], [])
            return line,

        def update(frame):
            line.set_data(range(frame + 1), data.y_data[:frame + 1])
            self.ax.set_xlim(0, len(data.y_data))
            
            y_min, y_max = min(data.y_data), max(data.y_data)
            if y_min == y_max:
                self.ax.set_ylim(y_min - 1, y_max + 1)
            else:
                margin = (y_max - y_min) * 0.1
                self.ax.set_ylim(y_min - margin, y_max + margin)
            return line,

        self.ani = animation.FuncAnimation(
            self.figure, update, frames=len(data.y_data),
            init_func=init, blit=True, repeat=False, interval=200
        )
        self.canvas.draw()

    def plot_root_convergence(self, steps: List[NumericalStep]):
        """Log-log or semi-log plot of errors vs iterations."""
        self.ax.clear()
        self._apply_dark_theme()
        
        iterations = [step.step_idx for step in steps]
        errors = [step.error if step.error is not None and step.error > 0 else 1e-15 for step in steps]
        
        self.ax.semilogy(iterations, errors, color=ACCENT_BLUE, marker='o', linewidth=2)
        self.ax.set_title("Root Convergence (Error vs Iteration)")
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Error (log scale)")
        self.ax.grid(True, which="both", linestyle='--', alpha=0.2)
        self.canvas.draw()

    def plot_solution_path(self, steps: List[NumericalStep], f_str: str):
        """2D plot showing the sequence of guesses on the function curve."""
        self.ax.clear()
        self._apply_dark_theme()
        
        f = SymbolicParser.parse_expression(f_str)
        
        guesses = [step.value for step in steps]
        if not guesses: return
        
        x_min, x_max = min(guesses), max(guesses)
        margin = max(abs(x_max - x_min) * 0.5, 1.0)
        x_vals = np.linspace(x_min - margin, x_max + margin, 400)
        y_vals = [f(x) for x in x_vals]
        
        self.ax.plot(x_vals, y_vals, color='white', alpha=0.4, label=f"f(x) = {f_str}")
        self.ax.axhline(0, color=ACCENT_ORANGE, linestyle='--', alpha=0.5)
        
        # Plot path
        path_y = [f(x) for x in guesses]
        self.ax.plot(guesses, path_y, color=ACCENT_BLUE, marker='x', linestyle='-', linewidth=1, label="Search Path")
        
        # Highlight root
        self.ax.scatter(guesses[-1], path_y[-1], color='#4caf50', s=100, zorder=5, label="Final Root")
        
        self.ax.set_title("Solution Path on f(x)")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.legend()
        self.canvas.draw()

    def plot_interpolation_result(self, points: List[tuple], polynomial_f: Callable, target_x: Optional[float] = None):
        """Data points vs fitted curve."""
        self.ax.clear()
        self._apply_dark_theme()
        
        x_pts, y_pts = zip(*points)
        
        x_min, x_max = min(x_pts), max(x_pts)
        margin = (x_max - x_min) * 0.2 or 1.0
        x_vals = np.linspace(x_min - margin, x_max + margin, 400)
        y_vals = [polynomial_f(x) for x in x_vals]
        
        self.ax.plot(x_vals, y_vals, color=ACCENT_BLUE, linewidth=2, label="Interpolation Polynomial")
        self.ax.scatter(x_pts, y_pts, color=ACCENT_ORANGE, s=50, zorder=5, label="Data Points")
        
        if target_x is not None:
            target_y = polynomial_f(target_x)
            self.ax.scatter([target_x], [target_y], color='#f44336', s=100, zorder=6, label=f"Target (x={target_x})")

        self.ax.set_title("Interpolation Result")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()
        self.canvas.draw()

    def plot_integration_area(self, f_str: str, a: float, b: float, method: str):
        """Visualize the area under the curve (rectangles, trapezoids)."""
        self.ax.clear()
        self._apply_dark_theme()
        
        f = SymbolicParser.parse_expression(f_str)
        
        margin = (b - a) * 0.2 or 1.0
        x_vals = np.linspace(a - margin, b + margin, 400)
        y_vals = [f(x) for x in x_vals]
        
        self.ax.plot(x_vals, y_vals, color='white', linewidth=2)
        
        # Fill area
        ix = np.linspace(a, b, 100)
        iy = [f(x) for x in ix]
        self.ax.fill_between(ix, iy, color=ACCENT_BLUE, alpha=0.3, label=f"Area ({method})")
        
        self.ax.set_title(f"Numerical Integration: {method}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.legend()
        self.canvas.draw()

    def plot_iteration_history(self, steps: List[NumericalStep]):
        """Error decay for linear systems or root finding."""
        self.ax.clear()
        self._apply_dark_theme()
        
        iterations = [step.step_idx for step in steps]
        errors = [step.error if step.error is not None else 0 for step in steps]
        
        self.ax.plot(iterations, errors, color=ACCENT_BLUE, marker='o', linewidth=2)
        self.ax.set_title("Iteration Error History")
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Error")
        self.canvas.draw()

    def plot_derivative_tangent(self, f_str: str, x0: float, derivative: float):
        """Show tangent line at x0."""
        self.ax.clear()
        self._apply_dark_theme()
        
        f = SymbolicParser.parse_expression(f_str)
        y0 = f(x0)
        
        # Tangent line: y = f(x0) + f'(x0) * (x - x0)
        x_vals = np.linspace(x0 - 2, x0 + 2, 400)
        y_vals = [f(x) for x in x_vals]
        
        tangent_y = [y0 + derivative * (x - x0) for x in x_vals]
        
        self.ax.plot(x_vals, y_vals, color='white', linewidth=2, label=f"f(x) = {f_str}")
        self.ax.plot(x_vals, tangent_y, color=ACCENT_ORANGE, linestyle='--', label=f"Tangent (m={derivative:.4f})")
        self.ax.scatter(x0, y0, color='#f44336', s=50, zorder=5)
        
        self.ax.set_title(f"Derivative at x={x0}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.legend()
        self.canvas.draw()

    def plot_vector_field(self, A: List[List[float]], b: List[float]):
        """For 2x2 systems, visualize the linear equations as lines and solution as intersection."""
        self.ax.clear()
        self._apply_dark_theme()
        
        if len(A) != 2 or len(A[0]) != 2:
            self.ax.text(0.5, 0.5, "Vector field only for 2x2 systems", ha='center', va='center', color='white')
            self.canvas.draw()
            return

        x_vals = np.linspace(-10, 10, 100)
        
        try:
            # Equation 1: A[0][0]*x + A[0][1]*y = b[0]
            if abs(A[0][1]) > 1e-12:
                y1 = (b[0] - A[0][0] * x_vals) / A[0][1]
                self.ax.plot(x_vals, y1, label=f"{A[0][0]}x + {A[0][1]}y = {b[0]}")
            else:
                x_const = b[0] / A[0][0]
                self.ax.axvline(x_const, label=f"{A[0][0]}x = {b[0]}")

            # Equation 2: A[1][0]*x + A[1][1]*y = b[1]
            if abs(A[1][1]) > 1e-12:
                y2 = (b[1] - A[1][0] * x_vals) / A[1][1]
                self.ax.plot(x_vals, y2, label=f"{A[1][0]}x + {A[1][1]}y = {b[1]}")
            else:
                x_const = b[1] / A[1][0]
                self.ax.axvline(x_const, label=f"{A[1][0]}x = {b[1]}")
            
            # Solve for intersection
            sol = np.linalg.solve(A, b)
            self.ax.scatter(sol[0], sol[1], color='#f44336', s=100, zorder=5, label="Solution")
            
            # Adjust limits
            self.ax.set_xlim(sol[0]-5, sol[0]+5)
            self.ax.set_ylim(sol[1]-5, sol[1]+5)
            
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', color='white')

        self.ax.set_title("Linear System Visualization")
        self.ax.set_xlabel("x1")
        self.ax.set_ylabel("x2")
        self.ax.legend()
        self.canvas.draw()

    def export_plot(self, filename: str):
        """Exports the current figure to a file."""
        self.figure.savefig(filename)
