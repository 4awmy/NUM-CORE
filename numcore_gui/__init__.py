import os
import matplotlib.pyplot as plt
from numcore_gui.dashboard import Dashboard

def launch_gui():
    """
    Launches the Graphical User Interface for NUM-CORE.
    Registers the True Black Matplotlib style before starting the app.
    """
    style_path = os.path.join(os.path.dirname(__file__), "styles", "numcore_black.mplstyle")
    if os.path.exists(style_path):
        plt.style.use(style_path)

    app = Dashboard()
    app.mainloop()
