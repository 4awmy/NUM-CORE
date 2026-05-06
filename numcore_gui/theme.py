"""
NUM-CORE Theme Configuration.
Defines the color palette and styling for the CustomTkinter GUI.
Supports both light and dark themes.
"""

import customtkinter as ctk

# Dark Theme Colors
DARK_BG = "#000000"
DARK_PANEL = "#111111"
DARK_BORDER = "#333333"
DARK_TEXT_PRIMARY = "#ffffff"
DARK_TEXT_SECONDARY = "#aaaaaa"

# Light Theme Colors
LIGHT_BG = "#f5f5f5"
LIGHT_PANEL = "#ffffff"
LIGHT_BORDER = "#e0e0e0"
LIGHT_TEXT_PRIMARY = "#000000"
LIGHT_TEXT_SECONDARY = "#666666"

# Accent Colors (consistent across themes)
ACCENT_BLUE = "#4fc3f7"
ACCENT_ORANGE = "#ff9800"
SUCCESS = "#4caf50"
ERROR = "#f44336"
WARN = "#ff9800"

# UI Constants
CORNER_RADIUS = 10
PADDING = 20
FONT_FAMILY = "Segoe UI"

# Dynamic color getters based on appearance mode
def get_bg_color():
    """Get background color based on current appearance mode."""
    mode = ctk.get_appearance_mode()
    return DARK_BG if mode == "Dark" else LIGHT_BG

def get_panel_color():
    """Get panel color based on current appearance mode."""
    mode = ctk.get_appearance_mode()
    return DARK_PANEL if mode == "Dark" else LIGHT_PANEL

def get_border_color():
    """Get border color based on current appearance mode."""
    mode = ctk.get_appearance_mode()
    return DARK_BORDER if mode == "Dark" else LIGHT_BORDER

def get_text_primary_color():
    """Get primary text color based on current appearance mode."""
    mode = ctk.get_appearance_mode()
    return DARK_TEXT_PRIMARY if mode == "Dark" else LIGHT_TEXT_PRIMARY

def get_text_secondary_color():
    """Get secondary text color based on current appearance mode."""
    mode = ctk.get_appearance_mode()
    return DARK_TEXT_SECONDARY if mode == "Dark" else LIGHT_TEXT_SECONDARY

# Backwards compatibility - old constant names (deprecated, use getters above)
BLACK = DARK_BG
PANEL = DARK_PANEL
BORDER = DARK_BORDER
TEXT_PRIMARY = DARK_TEXT_PRIMARY
TEXT_SECONDARY = DARK_TEXT_SECONDARY
