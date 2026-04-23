import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import customtkinter as ctk
from numcore_engine.models import SimulationData

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

        # Create Figure and Axes with dark theme
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
        self.figure.patch.set_facecolor('#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')

    def _style_toolbar(self):
        """Attempts to style the standard Tkinter toolbar to match the dark theme."""
        self.toolbar.config(background='#2b2b2b')
        for child in self.toolbar.winfo_children():
            try:
                child.config(background='#2b2b2b', foreground='white')
            except:
                pass

    def plot_static(self, data: SimulationData):
        """Renders a static plot from SimulationData."""
        self.ax.clear()
        self.ax.plot(data.x_data, data.y_data, color='#1f538d', linewidth=2, marker='o', markersize=4)
        self.ax.set_title(data.title)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.canvas.draw()

    def animate_convergence(self, data: SimulationData):
        """Creates a 'live' animation of convergence tracking."""
        self.ax.clear()
        line, = self.ax.plot([], [], color='#1f538d', linewidth=2, marker='o')
        self.ax.set_title(data.title)
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Value")
        self.ax.grid(True, linestyle='--', alpha=0.3)

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

    def plot_heatmap(self, data: SimulationData):
        """Renders a heatmap for matrix/network solutions if matrix is in metadata."""
        self.ax.clear()
        matrix = data.metadata.get("matrix")
        if matrix:
            im = self.ax.imshow(matrix, cmap='viridis')
            self.figure.colorbar(im, ax=self.ax)
            self.ax.set_title(data.title)
        else:
            self.plot_static(data)
        self.canvas.draw()

    def export_plot(self, filename: str):
        """Exports the current figure to a file."""
        self.figure.savefig(filename)
