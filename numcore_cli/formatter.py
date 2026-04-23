from typing import List, Optional

from rich.console import Console
from rich.table import Table

from numcore_engine.models import NumericalStep


class NumericalFormatter:
    """
    Implementation of NumericalFormatter to display solver steps in a clean rich.table.Table.
    """

    @staticmethod
    def format_steps(steps: List[NumericalStep], title: Optional[str] = None) -> Table:
        """
        Format a list of NumericalStep objects into a rich Table.

        Args:
            steps: The list of numerical steps to format.
            title: Optional title for the table.

        Returns:
            A rich Table object.
        """
        if not steps:
            return Table(title=title or "Numerical Steps", show_header=True)

        # Create the table
        table = Table(title=title or "Numerical Steps", show_header=True, header_style="bold magenta")

        # Add standard columns
        table.add_column("Step", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", justify="center", style="green")
        table.add_column("Error", justify="center", style="yellow")

        # Identify all unique detail keys across all steps
        detail_keys = set()
        for step in steps:
            detail_keys.update(step.details.keys())

        # Sort detail keys for consistent column order
        sorted_detail_keys = sorted(list(detail_keys))

        # Add detail columns
        for key in sorted_detail_keys:
            table.add_column(key, justify="center", style="blue")

        # Add rows
        for step in steps:
            row = [
                str(step.step_idx),
                f"{step.value:.8f}",
                f"{step.error:.8e}" if step.error is not None else "N/A",
            ]

            # Add detail values
            for key in sorted_detail_keys:
                val = step.details.get(key)
                if val is not None:
                    if isinstance(val, float):
                        row.append(f"{val:.8f}")
                    else:
                        row.append(str(val))
                else:
                    row.append("-")

            table.add_row(*row)

        return table

    @staticmethod
    def display_steps(steps: List[NumericalStep], title: Optional[str] = None) -> None:
        """
        Format and print the steps to the console.

        Args:
            steps: The list of numerical steps to display.
            title: Optional title for the table.
        """
        console = Console()
        table = NumericalFormatter.format_steps(steps, title)
        console.print(table)
