"""
NUM-CORE Theme Configuration.
Defines the color palette and styling for the CustomTkinter GUI.
"""

import customtkinter as ctk

# Color Palette
BLACK = "#000000"
ACCENT_BLUE = "#4fc3f7"
ACCENT_ORANGE = "#ff9800"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#aaaaaa"
SUCCESS = "#4caf50"
ERROR = "#f44336"
WARN = "#ffb74d"  # Changed to avoid collision with ACCENT_ORANGE
PANEL = "#111111"
BORDER = "#333333"

# UI Constants
CORNER_RADIUS = 10
PADDING = 20
FONT_FAMILY = "Segoe UI"

def apply_theme():
    """Registers the theme at the module level."""
    ctk.set_appearance_mode("dark")
    # In a real app, we might load a JSON theme file here
    # ctk.set_default_color_theme("path/to/theme.json")

