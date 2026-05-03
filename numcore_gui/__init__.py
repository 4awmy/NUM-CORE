import os
import matplotlib.pyplot as plt

# Register True Black style early so any import of PlotManager picks it up
_style = os.path.join(os.path.dirname(__file__), "styles", "numcore_black.mplstyle")
if os.path.exists(_style):
    plt.style.use(_style)

from numcore_gui.dashboard import Dashboard


def launch_gui():
    """
    Launches the Graphical User Interface for NUM-CORE.
    """
    app = Dashboard()
    app.mainloop()
