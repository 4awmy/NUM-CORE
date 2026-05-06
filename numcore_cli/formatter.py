import csv
from datetime import datetime
from typing import List, Optional, Any, Dict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from numcore_engine.models import NumericalStep


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
    # Bisection
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_bisection_steps(steps: List[NumericalStep]) -> None:
        """
        Iter | a | b | f(a) | f(b) | c | f(c) | |Error|
        """
        console = Console()
        table = Table(
            title="Bisection Method — Step-by-Step",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Iter", justify="center", style="bold white")
        table.add_column("a", justify="center")
        table.add_column("b", justify="center")
        table.add_column("f(a)", justify="center", style="green")
        table.add_column("f(b)", justify="center", style="green")
        table.add_column("c (mid)", justify="center", style="bold yellow")
        table.add_column("f(c)", justify="center", style="bold green")
        table.add_column("|Error|", justify="center", style="magenta")

        for step in steps:
            table.add_row(
                str(step.step_idx + 1),
                f"{step.details.get('a', 0):.6f}",
                f"{step.details.get('b', 0):.6f}",
                f"{step.details.get('f(a)', 0):.6f}",
                f"{step.details.get('f(b)', 0):.6f}",
                f"{step.details.get('c', 0):.6f}",
                f"{step.details.get('f(c)', 0):.6f}",
                f"{step.error:.4e}" if step.error is not None else "--",
            )
        console.print(table)

    # ──────────────────────────────────────────────────────────────
    # Secant
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_secant_steps(steps: List[NumericalStep]) -> None:
        """
        Iter | x0 | x1 | f(x0) | f(x1) | x2 | |Error|
        """
        console = Console()
        table = Table(
            title="Secant Method — Step-by-Step",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Iter", justify="center", style="bold white")
        table.add_column("x_n-1", justify="center")
        table.add_column("x_n", justify="center")
        table.add_column("f(x_n-1)", justify="center", style="green")
        table.add_column("f(x_n)", justify="center", style="green")
        table.add_column("x_n+1", justify="center", style="bold yellow")
        table.add_column("|Error|", justify="center", style="magenta")

        for step in steps:
            table.add_row(
                str(step.step_idx + 1),
                f"{step.details.get('x0', 0):.6f}",
                f"{step.details.get('x1', 0):.6f}",
                f"{step.details.get('f(x0)', 0):.6f}",
                f"{step.details.get('f(x1)', 0):.6f}",
                f"{step.details.get('x2', 0):.6f}",
                f"{step.error:.4e}" if step.error is not None else "--",
            )
        console.print(table)

    # ──────────────────────────────────────────────────────────────
    # Difference Tables
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_difference_table(steps: List[NumericalStep], title: str = "Forward Difference Table") -> None:
        """
        i | x_i | y_i | Δy_i | Δ²y_i | ...
        """
        if not steps:
            return
        
        console = Console()
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED,
            border_style="cyan",
        )
        
        table.add_column("i", justify="center", style="bold white")
        table.add_column("x_i", justify="center")
        table.add_column("y_i", justify="center", style="green")
        
        # Find max difference order
        max_order = 0
        for step in steps:
            for key in step.details.keys():
                if key.startswith("diff_") or key.startswith("dd_"):
                    order = int(key.split("_")[1])
                    max_order = max(max_order, order)
        
        prefix = "Δ" if "diff_1" in steps[0].details else "f["
        for j in range(1, max_order + 1):
            col_name = f"{prefix}^{j}y_i" if prefix == "Δ" else f"Order {j}"
            table.add_column(col_name, justify="center", style="blue")

        for step in steps:
            row = [
                str(step.step_idx),
                f"{step.details.get('x', 0):.4f}",
                f"{step.details.get('y', 0):.4f}",
            ]
            for j in range(1, max_order + 1):
                key = f"diff_{j}" if prefix == "Δ" else f"dd_{j}"
                val = step.details.get(key)
                row.append(f"{val:.4f}" if val is not None else "")
            table.add_row(*row)
            
        console.print(table)

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

    @staticmethod
    def display_euler_steps(steps: List[NumericalStep]) -> None:
        """
        Iter | x | y | f(x,y)
        """
        console = Console()
        table = Table(
            title="Euler's Method — Step-by-Step",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Iter", justify="center", style="bold white")
        table.add_column("x", justify="center")
        table.add_column("y", justify="center", style="bold yellow")
        table.add_column("f(x,y)", justify="center", style="green")

        for step in steps:
            table.add_row(
                str(step.step_idx),
                f"{step.details.get('x', 0):.6f}",
                f"{step.details.get('y', 0):.6f}",
                f"{step.details.get('f(x,y)', 0):.6f}",
            )
        
        console.print(table)

    @staticmethod
    def display_rk4_steps(steps: List[NumericalStep]) -> None:
        """
        Iter | x | y | k1 | k2 | k3 | k4
        """
        console = Console()
        table = Table(
            title="Runge-Kutta (RK4) — Step-by-Step",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Iter", justify="center", style="bold white")
        table.add_column("x", justify="center")
        table.add_column("y", justify="center", style="bold yellow")
        table.add_column("k1", justify="center")
        table.add_column("k2", justify="center")
        table.add_column("k3", justify="center")
        table.add_column("k4", justify="center")

        for step in steps:
            table.add_row(
                str(step.step_idx),
                f"{step.details.get('x', 0):.6f}",
                f"{step.details.get('y', 0):.6f}",
                f"{step.details.get('k1', 0):.6f}" if 'k1' in step.details else "—",
                f"{step.details.get('k2', 0):.6f}" if 'k2' in step.details else "—",
                f"{step.details.get('k3', 0):.6f}" if 'k3' in step.details else "—",
                f"{step.details.get('k4', 0):.6f}" if 'k4' in step.details else "—",
            )
        
        console.print(table)

    @staticmethod
    def display_least_squares_steps(steps: List[NumericalStep]) -> None:
        """
        Displays regression coefficients.
        """
        console = Console()
        if not steps:
            return
            
        details = steps[0].details
        table = Table(
            title="Least Squares Regression — Summary",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE_HEAD,
            border_style="cyan",
        )
        table.add_column("Metric", justify="left", style="bold white")
        table.add_column("Value", justify="right", style="bold yellow")

        table.add_row("Slope (m)", f"{details.get('slope', 0):.6f}")
        table.add_row("Intercept (c)", f"{details.get('intercept', 0):.6f}")
        table.add_row("Σx", f"{details.get('sum_x', 0):.6f}")
        table.add_row("Σy", f"{details.get('sum_y', 0):.6f}")
        table.add_row("Σx²", f"{details.get('sum_xx', 0):.6f}")
        table.add_row("Σxy", f"{details.get('sum_xy', 0):.6f}")
        
        console.print(table)

    # ──────────────────────────────────────────────────────────────
    # Numerical Integration
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def display_integration_table(steps: List[NumericalStep], title: str = "Integration Table") -> None:
        """
        i | x_i | y_i | Weight | Weighted y_i
        """
        if not steps:
            return
        
        console = Console()
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED,
            border_style="cyan",
        )
        
        table.add_column("i", justify="center", style="bold white")
        table.add_column("x_i", justify="center")
        table.add_column("y_i", justify="center", style="green")
        table.add_column("Weight", justify="center", style="blue")
        table.add_column("Weighted y_i", justify="center", style="bold yellow")

        for step in steps:
            table.add_row(
                str(step.step_idx),
                f"{step.details.get('x', 0):.4f}",
                f"{step.details.get('y', 0):.4f}",
                str(step.details.get('weight', 1)),
                f"{step.details.get('weighted_y', 0):.4f}",
            )
            
        console.print(table)

    @staticmethod
    def display_integration_steps(steps: List[NumericalStep], metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Shows integration formula breakdown:
        Method | h | n | Result
        """
        if not steps:
            return
        console = Console()
        
        # If metadata is provided, use it. Otherwise try to get from first step.
        if metadata:
            method = metadata.get("method", "Unknown")
            h = metadata.get("h_value", "?")
            n = metadata.get("n", "?")
            weighted_sum_str = metadata.get("weighted_sum_str", "")
            result = metadata.get("total_integral", 0.0)
        else:
            step = steps[0]
            method = step.details.get("method", "Unknown")
            h = step.details.get("h", "?")
            n = step.details.get("n", "?")
            weighted_sum_str = step.details.get("weighted_sum", "")
            result = step.value

        # Print the formula used
        formula_map = {
            "Trapezoidal Rule":    "I ~= (h/2) * [f(x0) + 2*sum(f(xi)) + f(xn)]",
            "Simpson's 1/3 Rule":  "I ~= (h/3) * [f(x0) + 4*sum(f(x_odd)) + 2*sum(f(x_even)) + f(xn)]",
            "Simpson's 3/8 Rule":  "I ~= (3h/8) * [f(x0) + 3*sum(f(x_3k+-1,2)) + 2*sum(f(x_3k)) + f(xn)]",
        }
        formula = formula_map.get(method, "See method definition")

        content = (
            f"[bold]Method:[/bold]   {method}\n"
            f"[bold]Formula:[/bold]  {formula}\n"
            f"[bold]Step h:[/bold]   {h:.6f}\n" if isinstance(h, (float, int)) else f"[bold]Step h:[/bold]   {h}\n"
        )
        
        if n != "?":
            content += f"[bold]Intervals n:[/bold] {n}\n"
            
        if weighted_sum_str:
            content += f"\n[bold]Weighted Sum:[/bold]\n{weighted_sum_str}\n"
            
        content += f"\n[bold green]Result = {result:.8f}[/bold green]"

        console.print(Panel(
            content,
            title="[bold cyan]Integration — Step Breakdown[/bold cyan]",
            border_style="cyan",
        ))

    @staticmethod
    def export_steps_to_csv(steps: List[NumericalStep], method_name: str, filename: Optional[str] = None) -> str:
        """
        Exports numerical steps to a CSV file.
        Columns: step_idx, value, error, plus all keys found in 'details'.
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{method_name.lower().replace(' ', '_')}_{timestamp}.csv"

        # Collect all unique detail keys
        detail_keys = sorted({k for step in steps for k in step.details.keys()})
        fieldnames = ["step_idx", "value", "error"] + detail_keys

        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for step in steps:
                row = {
                    "step_idx": step.step_idx,
                    "value": step.value,
                    "error": step.error if step.error is not None else "",
                }
                # Add details
                for key in detail_keys:
                    val = step.details.get(key, "")
                    # Handle list values (like in linear systems) by converting to string
                    if isinstance(val, list):
                        row[key] = str(val)
                    else:
                        row[key] = val
                writer.writerow(row)

        return filename
