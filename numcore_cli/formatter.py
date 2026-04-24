from typing import List, Optional, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from numcore_engine.models import NumericalStep

import csv


class NumericalFormatter:
    """
    Method-aware formatter that displays solver steps like a textbook solution.
    Each numerical method gets its own column layout so students can follow
    the work step-by-step exactly as done manually.
    """

    # ──────────────────────────────────────────────────────────────
    # Generic fallback
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def export_steps_to_csv(steps, filename, method):
        try:
            if not steps:
                print("No data to export.")
                return

            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                if not filename.endswith(".csv"):
                    filename += ".csv"

                # pega todas as chaves possíveis de details
                detail_keys = sorted({
                    key for step in steps for key in step.details.keys()
                })

                # cabeçalho
                headers = ["iteration", "value", "error"] + detail_keys
                writer.writerow(headers)

                # linhas
                for step in steps:
                    row = [
                        step.step_idx + 1,
                        step.value,
                        step.error if step.error is not None else ""
                    ]

                    for key in detail_keys:
                        val = step.details.get(key, "")
                        row.append(val)

                    writer.writerow(row)

            print(f"Saved: {filename}")

        except Exception as e:
            print(f"Error saving CSV: {e}")


    @staticmethod
    def format_steps(steps: List[NumericalStep], title: Optional[str] = None) -> Table:
        """Generic formatter — used when no method-specific formatter is called."""
        table = Table(
            title=title or "Numerical Steps",
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            border_style="dim",
        )
        table.add_column("Step", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", justify="center", style="green")
        table.add_column("Error", justify="center", style="yellow")

        detail_keys = sorted({k for step in steps for k in step.details.keys()})
        for key in detail_keys:
            table.add_column(key, justify="center", style="blue")

        for step in steps:
            row = [
                str(step.step_idx + 1),
                f"{step.value:.8f}",
                f"{step.error:.4e}" if step.error is not None else "—",
            ]
            for key in detail_keys:
                val = step.details.get(key)
                if val is None:
                    row.append("—")
                elif isinstance(val, float):
                    row.append(f"{val:.8f}")
                else:
                    row.append(str(val))
            table.add_row(*row)

        return table

    @staticmethod
    def display_steps(steps: List[NumericalStep], title: Optional[str] = None) -> None:
        """Display the generic step table."""
        Console().print(NumericalFormatter.format_steps(steps, title))

    # ──────────────────────────────────────────────────────────────
    # Newton-Raphson
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_newton_raphson_steps(steps: List[NumericalStep]) -> None:
        """
        Displays each N-R iteration exactly as written in a textbook:
        Iter | x_n | f(x_n) | f'(x_n) | x_{n+1} = x_n - f/f' | |Error|
        """
        console = Console()
        table = Table(
            title="Newton-Raphson — Step-by-Step",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Iter", justify="center", style="bold white", no_wrap=True)
        table.add_column("x_n", justify="center", style="white")
        table.add_column("f(x_n)", justify="center", style="green")
        table.add_column("f'(x_n)", justify="center", style="blue")
        table.add_column("x_{n+1}", justify="center", style="bold yellow")
        table.add_column("|Error|", justify="center", style="magenta")
        table.add_column("Status", justify="center", no_wrap=True)

        prev_x = steps[0].details.get("x_n", "?") if steps else "?"

        for step in steps:
            x_n    = step.details.get("x_n", "?")
            fx     = step.details.get("f(x)", "?")
            dfx    = step.details.get("f'(x)", "?")
            x_next = step.value
            err    = step.error

            converging = "[OK]" if (err is not None and err < 1e-4) else "..."
            status_style = "green" if converging == "[OK]" else "yellow"

            table.add_row(
                str(step.step_idx + 1),
                f"{x_n:.8f}"    if isinstance(x_n, float)  else str(x_n),
                f"{fx:.8f}"     if isinstance(fx, float)    else str(fx),
                f"{dfx:.8f}"    if isinstance(dfx, float)   else str(dfx),
                f"{x_next:.8f}",
                f"{err:.4e}"    if err is not None          else "--",
                Text(converging, style=status_style),
            )
        
        console.print(table)

    # ──────────────────────────────────────────────────────────────
    # Simple Iteration (Fixed Point)
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_simple_iteration_steps(steps: List[NumericalStep]) -> None:
        """
        Iter | x_n | g(x_n) = x_{n+1} | |Error|
        """
        console = Console()
        table = Table(
            title="Simple Iteration — Step-by-Step",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Iter",         justify="center", style="bold white", no_wrap=True)
        table.add_column("x_n",          justify="center", style="white")
        table.add_column("g(x_n) = x_{n+1}", justify="center", style="bold yellow")
        table.add_column("|Error|",       justify="center", style="magenta")
        table.add_column("Status",        justify="center", no_wrap=True)

        for step in steps:
            x_n   = step.details.get("x_n", "?")
            g_xn  = step.details.get("g(x)", step.value)
            err   = step.error
            converging = "[OK]" if (err is not None and err < 1e-4) else "..."

            table.add_row(
                str(step.step_idx + 1),
                f"{x_n:.8f}"  if isinstance(x_n, float)  else str(x_n),
                f"{g_xn:.8f}" if isinstance(g_xn, float) else str(g_xn),
                f"{err:.4e}"  if err is not None          else "--",
                Text(converging, style="green" if converging == "[OK]" else "yellow"),
            )

        console.print(table)

    # ──────────────────────────────────────────────────────────────
    # Linear Systems (Gauss-Seidel / Jacobi)
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_linear_steps(steps: List[NumericalStep], method_name: str = "Iterative") -> None:
        """
        Iter | x1 | x2 | ... | xn | Max |Error|
        Column count is inferred from the first step's 'x' detail.
        """
        if not steps:
            return

        console = Console()
        n_vars = len(steps[0].details.get("x", []))

        table = Table(
            title=f"{method_name} — Step-by-Step",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Iter", justify="center", style="bold white", no_wrap=True)
        for i in range(n_vars):
            table.add_column(f"x{i+1}", justify="center", style="green")
        table.add_column("Max |Error|", justify="center", style="magenta")
        table.add_column("Status",      justify="center", no_wrap=True)

        for step in steps:
            x_vals = step.details.get("x", [])
            err    = step.error
            converging = "[OK]" if (err is not None and err < 1e-4) else "..."
            row = [str(step.step_idx + 1)]
            for v in x_vals:
                row.append(f"{v:.6f}" if isinstance(v, float) else str(v))
            row.append(f"{err:.4e}" if err is not None else "—")
            row.append(Text(converging, style="green" if converging == "✓" else "yellow"))
            table.add_row(*row)

        console.print(table)

    # ──────────────────────────────────────────────────────────────
    # Newton's Divided Difference Interpolation
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_interpolation_steps(steps: List[NumericalStep]) -> None:
        """
        Shows the divided-difference coefficient table:
        Order | Indices | Divided Difference Coefficient
        """
        console = Console()
        table = Table(
            title="Newton's Divided Difference — Coefficient Table",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Order", justify="center", style="bold white")
        table.add_column("Indices Used", justify="center", style="blue")
        table.add_column("Coefficient", justify="center", style="bold yellow")
        table.add_column("Role in Polynomial", justify="left", style="dim")

        for step in steps:
            order   = step.step_idx
            indices = step.details.get("indices", [])
            coef    = step.value
            if order == 0:
                role = "f[x0]  -- constant term"
            elif order == 1:
                role = "f[x0,x1] -- slope"
            else:
                role = f"f[x0...x_{order}] -- order-{order} correction"

            table.add_row(
                str(order),
                str(indices),
                f"{coef:.8f}",
                role,
            )

        console.print(table)

    # ──────────────────────────────────────────────────────────────
    # Numerical Integration
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_integration_steps(steps: List[NumericalStep]) -> None:
        """
        Shows integration formula breakdown:
        Method | h | n | Result
        """
        if not steps:
            return
        console = Console()
        step    = steps[0]
        method  = step.details.get("method", "Unknown")
        h       = step.details.get("h", "?")
        n       = step.details.get("n", "?")
        result  = step.value

        # Print the formula used
        formula_map = {
                "Trapezoidal Rule":    "I ~= (h/2) * [f(x0) + 2*sum(f(xi)) + f(xn)]",
            "Simpson's 1/3 Rule":  "I ~= (h/3) * [f(x0) + 4*sum(f(x_odd)) + 2*sum(f(x_even)) + f(xn)]",
            "Simpson's 3/8 Rule":  "I ~= (3h/8) * [f(x0) + 3*sum(f(x_3k+-1,2)) + 2*sum(f(x_3k)) + f(xn)]",
        }
        formula = formula_map.get(method, "See method definition")

        summary = (
            f"[bold]Method:[/bold]   {method}\n"
            f"[bold]Formula:[/bold]  {formula}\n"
            f"[bold]h (step):[/bold] {h:.6f}" if isinstance(h, float) else f"[bold]h:[/bold] {h}"
        )
        console.print(Panel(
            f"[bold]Method:[/bold]   {method}\n"
            f"[bold]Formula:[/bold]  {formula}\n"
            f"[bold]Step h:[/bold]   {h:.6f}\n"
            f"[bold]Intervals n:[/bold] {n}\n\n"
            f"[bold green]Result = {result:.8f}[/bold green]",
            title="[bold cyan]Integration — Step Breakdown[/bold cyan]",
            border_style="cyan",
        ))