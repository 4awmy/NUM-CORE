"""Tests for the run_comparison() method in NumericalCLI."""
import pytest
from unittest.mock import patch, MagicMock

from numcore_cli.terminal import NumericalCLI


# ---------------------------------------------------------------------------
# Shared test matrix (diagonally dominant 3×3)
# ---------------------------------------------------------------------------
_A = [[4.0, -1.0, -1.0], [-1.0, 4.0, -1.0], [-1.0, -1.0, 4.0]]
_b = [3.0, 2.0, 1.0]
_x0_str = "0 0 0"


def _make_example_inputs():
    """Return the side_effect lists for mocking prompts in example mode."""
    # Prompt.ask calls: "Load engineering example?" -> "y", verbose -> "n", press Enter -> ""
    prompt_calls = ["y", "n", ""]
    # IntPrompt.ask: none needed for example mode
    int_calls = []
    # FloatPrompt.ask: none needed for example mode
    float_calls = []
    return prompt_calls, int_calls, float_calls


def _make_manual_inputs(n=3):
    """Return side_effect lists for manual (non-example) mode."""
    # Prompt.ask: "Load example?" -> "n",
    #             n rows of coefficients, b vector, initial guess,
    #             verbose -> "n", press Enter -> ""
    rows = [" ".join(map(str, row)) for row in _A]
    b_str = " ".join(map(str, _b))
    prompt_calls = ["n"] + rows + [b_str, _x0_str, "n", ""]
    int_calls = [3, 100]      # n=3, max_iter=100
    float_calls = [1e-6]      # tol
    return prompt_calls, int_calls, float_calls


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRunComparison:
    def setup_method(self):
        self.cli = NumericalCLI()

    def test_comparison_example_mode_runs_without_error(self):
        """run_comparison() with example data should complete without raising."""
        prompt_calls, int_calls, float_calls = _make_example_inputs()
        with patch("numcore_cli.terminal.Prompt.ask", side_effect=prompt_calls), \
             patch("numcore_cli.terminal.IntPrompt.ask", side_effect=int_calls), \
             patch("numcore_cli.terminal.FloatPrompt.ask", side_effect=float_calls), \
             patch.object(self.cli.console, "print"):
            # Should not raise
            self.cli.run_comparison()

    def test_comparison_example_mode_prints_table(self):
        """run_comparison() should print a Rich table to the console."""
        prompt_calls, int_calls, float_calls = _make_example_inputs()
        printed_items = []
        with patch("numcore_cli.terminal.Prompt.ask", side_effect=prompt_calls), \
             patch("numcore_cli.terminal.IntPrompt.ask", side_effect=int_calls), \
             patch("numcore_cli.terminal.FloatPrompt.ask", side_effect=float_calls), \
             patch.object(self.cli.console, "print", side_effect=lambda *a, **kw: printed_items.extend(a)):
            self.cli.run_comparison()

        from rich.table import Table
        tables = [item for item in printed_items if isinstance(item, Table)]
        assert len(tables) >= 1, "Expected at least one Rich Table to be printed"
        titles = [t.title for t in tables]
        assert any("Comparison" in (t or "") for t in titles), (
            f"Expected a comparison table, got titles: {titles}"
        )

    def test_comparison_verbose_shows_step_tables(self):
        """When the user requests verbose output, step-by-step tables are shown."""
        # verbose -> "y"
        prompt_calls = ["y", "y", ""]
        with patch("numcore_cli.terminal.Prompt.ask", side_effect=prompt_calls), \
             patch("numcore_cli.terminal.IntPrompt.ask", side_effect=[]), \
             patch("numcore_cli.terminal.FloatPrompt.ask", side_effect=[]), \
             patch.object(self.cli.formatter, "display_linear_steps") as mock_display, \
             patch.object(self.cli.console, "print"):
            self.cli.run_comparison()

        # Should be called twice: once for Jacobi, once for Gauss-Seidel
        assert mock_display.call_count == 2
        method_names = [call.kwargs.get("method_name") or call.args[1]
                        for call in mock_display.call_args_list]
        assert "Jacobi" in method_names
        assert "Gauss-Seidel" in method_names

    def test_comparison_manual_mode_runs_without_error(self):
        """run_comparison() in manual input mode should complete without raising."""
        prompt_calls, int_calls, float_calls = _make_manual_inputs()
        with patch("numcore_cli.terminal.Prompt.ask", side_effect=prompt_calls), \
             patch("numcore_cli.terminal.IntPrompt.ask", side_effect=int_calls), \
             patch("numcore_cli.terminal.FloatPrompt.ask", side_effect=float_calls), \
             patch.object(self.cli.console, "print"):
            self.cli.run_comparison()

    def test_network_menu_has_compare_option(self):
        """network_solver_menu() should offer option 3 'Compare Both Methods'."""
        # choices: pick 3 (compare), then 4 (back)
        with patch("numcore_cli.terminal.IntPrompt.ask", side_effect=[3, 4]), \
             patch.object(self.cli, "run_comparison") as mock_comp, \
             patch.object(self.cli, "clear_screen"), \
             patch.object(self.cli, "display_header"), \
             patch.object(self.cli, "display_menu_options"):
            self.cli.network_solver_menu()

        mock_comp.assert_called_once()
