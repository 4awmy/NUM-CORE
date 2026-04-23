import pytest
from unittest.mock import patch, MagicMock
import customtkinter as ctk

# We mock the GUI components to avoid TclErrors in headless environments
@pytest.fixture(autouse=True)
def mock_ctk():
    with patch('customtkinter.CTk.__init__', return_value=None), \
         patch('customtkinter.CTkFrame.__init__', return_value=None), \
         patch('customtkinter.CTkLabel.__init__', return_value=None), \
         patch('customtkinter.CTkButton.__init__', return_value=None), \
         patch('customtkinter.CTkEntry.__init__', return_value=None), \
         patch('customtkinter.CTkTextbox.__init__', return_value=None), \
         patch('customtkinter.CTkOptionMenu.__init__', return_value=None), \
         patch('customtkinter.CTkFont'), \
         patch('customtkinter.CTk.grid'), \
         patch('customtkinter.CTkFrame.grid'), \
         patch('customtkinter.CTkLabel.grid'), \
         patch('customtkinter.CTkButton.grid'), \
         patch('customtkinter.CTkEntry.grid'), \
         patch('customtkinter.CTkTextbox.grid'), \
         patch('customtkinter.CTkOptionMenu.grid'), \
         patch('customtkinter.CTkFrame.grid_rowconfigure'), \
         patch('customtkinter.CTkFrame.grid_columnconfigure'), \
         patch('customtkinter.CTk.grid_rowconfigure'), \
         patch('customtkinter.CTk.grid_columnconfigure'), \
         patch('customtkinter.CTkFrame.grid_forget'), \
         patch('customtkinter.CTkFrame.pack'), \
         patch('customtkinter.CTkLabel.pack'), \
         patch('customtkinter.set_appearance_mode'):
        yield

from numcore_cli.terminal import NumericalCLI
from numcore_gui.dashboard import Dashboard
from numcore_engine.solvers import NewtonRaphsonSolver

def test_cli_menu_navigation():
    """Tests that the CLI menu correctly routes to different categories and exits."""
    cli = NumericalCLI()
    with patch('numcore_cli.terminal.Prompt.ask', side_effect=["Root Finding", "Back", "Exit"]):
        with patch.object(cli, 'root_finding_menu', wraps=cli.root_finding_menu) as mock_root_menu:
            cli.main_menu()
            mock_root_menu.assert_called_once()

def test_gui_initialization_and_transitions():
    """Tests that the GUI dashboard initializes correctly and can switch pages."""
    app = Dashboard()
    
    # Verify all pages are initialized
    assert "root_finder" in app.pages
    assert "network_solver" in app.pages
    assert "calculus" in app.pages
    
    # Test transitions
    app.show_network_solver()
    app.show_calculus()
    app.show_root_finder()

def test_help_system_integration():
    """Verifies that help buttons are correctly injected into GUI pages."""
    app = Dashboard()
    
    # Check Dashboard sidebar help button
    assert hasattr(app, 'help_button')
    
    # Check Root Finder page help button
    root_page = app.pages["root_finder"]
    assert hasattr(root_page, 'help_button')
    
    # Check Network Solver page help buttons
    network_page = app.pages["network_solver"]
    assert hasattr(network_page, 'help_button')
    assert hasattr(network_page, 'diag_help_button')

    # Check Calculus page help button
    calculus_page = app.pages["calculus"]
    assert hasattr(calculus_page, 'help_button')

def test_end_to_end_numerical_flow_cli():
    """Verifies a full numerical solver flow through the CLI."""
    cli = NumericalCLI()
    with patch('numcore_cli.terminal.Prompt.ask', side_effect=["Root Finding", "Newton-Raphson", "x**2 - 2", "Back", "Exit"]), \
         patch('numcore_cli.terminal.FloatPrompt.ask', side_effect=[1.0, 1e-6]), \
         patch('numcore_cli.terminal.IntPrompt.ask', side_effect=[100]):
        
        with patch.object(cli.console, 'print'):
            cli.main_menu()
