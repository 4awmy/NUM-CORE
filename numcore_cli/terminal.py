import sys
import os
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

from numcore_engine.solvers import (
    NewtonRaphsonSolver,
    SimpleIterationSolver,
    GaussSeidelSolver,
    JacobiSolver,
    EulerSolver,
    ModifiedEulerSolver,
    RungeKuttaSolver,
    TaylorSeriesOrder4Solver,
    LeastSquaresSolver,
    CurveFittingSolver,
    GaussianQuadratureSolver,
    NumericalDifferentiationSolver,
)
from numcore_engine.solvers.calculus_engine import (
    InterpolationSolver,
    IntegrationSolver,
)
from .formatter import NumericalFormatter


class NumericalCLI:
    """
    Refactored CLI with Gemini-style numbered menus and preloaded examples.
    """

    def __init__(self):
        self.console = Console()
        self.formatter = NumericalFormatter()
        self.last_steps: List[Any] = []
        self.theme_color = "cyan"
        self.accent_color = "bold magenta"

    def get_steps_from_result(self) -> List[Any]:
        """Return the steps from the last executed solver."""
        return self.last_steps

    def ask_export(self, steps: List[Any], method_name: str):
        """Offer CSV export for the given steps."""
        if not steps:
            return
            
        if Prompt.ask("\nExport steps to CSV? (y/n)", choices=["y", "n"], default="n") == "y":
            filename = self.formatter.export_steps_to_csv(steps, method_name)
            self.console.print(f"[bold green]Successfully exported to {filename}[/bold green]")

    def clear_screen(self):
        """Clear the terminal screen."""
        self.console.clear()

    def display_header(self, title: str, subtitle: Optional[str] = None):
        """Display a consistent header for all screens."""
        header_text = Text()
        header_text.append(f" {title} ", style=f"bold white on {self.theme_color}")
        if subtitle:
            header_text.append(f"\n{subtitle}", style="italic dim")
        
        self.console.print(Align.center(Panel(
            header_text,
            border_style=self.theme_color,
            padding=(1, 2),
            expand=False
        )))
        self.console.print()

    def display_menu_options(self, options: List[str]):
        """Display a numbered list of options in a clean panel."""
        menu_table = Table.grid(padding=(0, 1))
        for i, option in enumerate(options, 1):
            menu_table.add_row(
                Text(f"{i}.", style=self.accent_color),
                Text(option, style="white")
            )
        
        self.console.print(Panel(
            menu_table,
            title="[bold]Select an Option[/bold]",
            title_align="left",
            border_style="dim",
            padding=(1, 2)
        ))

    def main_menu(self):
        """Main menu loop."""
        while True:
            self.clear_screen()
            self.display_header(
                "NUM-CORE",
                "Professional Numerical Computation Suite"
            )
            
            options = [
                "Root Finding (Newton-Raphson, Simple Iteration)",
                "Linear Systems (Gauss-Seidel, Jacobi)",
                "Calculus (Interpolation, Integration)",
                "ODE & Regression (Euler, RK4, Least Squares)",
                "Exit"
            ]
            self.display_menu_options(options)
            
            choice = IntPrompt.ask(
                "Enter your choice",
                choices=[str(i) for i in range(1, len(options) + 1)],
                show_choices=False
            )

            if choice == 1:
                self.root_finding_menu()
            elif choice == 2:
                self.network_solver_menu()
            elif choice == 3:
                self.calculus_menu()
            elif choice == 4:
                self.ode_regression_menu()
            elif choice == 5:
                self.console.print("[bold yellow]Exiting NUM-CORE. Goodbye![/bold yellow]")
                break

    def ode_regression_menu(self):
        """ODE and Regression submenu."""
        while True:
            self.clear_screen()
            self.display_header("ODE & Regression", "Solve Differential Equations and Fit Data")
            
            options = [
                "Euler's Method (ODE)",
                "Modified Euler's Method (Heun)",
                "Runge-Kutta Method (RK4)",
                "Taylor Series Method (Order 4)",
                "Least Squares Regression (Linear)",
                "Curve Fitting (Quadratic, Power, etc.)",
                "Back to Main Menu"
            ]
            self.display_menu_options(options)
            
            choice = IntPrompt.ask(
                "Enter your choice",
                choices=[str(i) for i in range(1, len(options) + 1)],
                show_choices=False
            )

            if choice == 1:
                self.run_euler()
            elif choice == 2:
                self.run_modified_euler()
            elif choice == 3:
                self.run_rk4()
            elif choice == 4:
                self.run_taylor_series()
            elif choice == 5:
                self.run_least_squares()
            elif choice == 6:
                self.run_curve_fitting()
            elif choice == 7:
                break

    def run_modified_euler(self):
        """Run Modified Euler's method solver."""
        self.clear_screen()
        self.display_header("Modified Euler (Heun)", "Second-order ODE Solver")
        
        self.console.print(Panel(
            "Modified Euler's method (Heun's method) improves on Euler's method by using a "
            "predictor-corrector approach to achieve second-order accuracy.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            expression = "x + y"
            x0, y0 = 0.0, 1.0
            h = 0.1
            steps = 10
            self.console.print(f"[bold cyan]Example: dy/dx = x + y, y(0) = 1[/bold cyan]")
        else:
            expression = Prompt.ask("Enter dy/dx = f(x, y) (e.g., x + y)")
            x0 = FloatPrompt.ask("Enter initial x0", default=0.0)
            y0 = FloatPrompt.ask("Enter initial y0", default=1.0)
            h = FloatPrompt.ask("Enter step size h", default=0.1)
            steps = IntPrompt.ask("Enter number of steps", default=10)

        solver = ModifiedEulerSolver()
        try:
            result = solver.solve(expression=expression, x0=x0, y0=y0, h=h, steps=steps)
            self.last_steps = solver.get_steps()
            self.formatter.display_euler_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Final y value: {result.y_data[-1]:.8f}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Modified-Euler")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_taylor_series(self):
        """Run Taylor Series method solver."""
        self.clear_screen()
        self.display_header("Taylor Series (Order 4)", "High-order ODE Solver")
        
        self.console.print(Panel(
            "The Taylor Series method uses higher-order derivatives of the function to achieve "
            "extremely high accuracy. This implementation uses a 4th-order expansion.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            expression = "x + y"
            x0, y0 = 0.0, 1.0
            h = 0.1
            steps = 10
            self.console.print(f"[bold cyan]Example: dy/dx = x + y, y(0) = 1[/bold cyan]")
        else:
            expression = Prompt.ask("Enter dy/dx = f(x, y) (e.g., x + y)")
            x0 = FloatPrompt.ask("Enter initial x0", default=0.0)
            y0 = FloatPrompt.ask("Enter initial y0", default=1.0)
            h = FloatPrompt.ask("Enter step size h", default=0.1)
            steps = IntPrompt.ask("Enter number of steps", default=10)

        solver = TaylorSeriesOrder4Solver()
        try:
            result = solver.solve(expression=expression, x0=x0, y0=y0, h=h, steps=steps)
            self.last_steps = solver.get_steps()
            self.formatter.display_rk4_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Final y value: {result.y_data[-1]:.8f}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Taylor-Series")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_curve_fitting(self):
        """Run Curve Fitting regression solver."""
        self.clear_screen()
        self.display_header("Curve Fitting", "Non-linear Regression")
        
        self.console.print(Panel(
            "Fits data to non-linear models like Quadratic (y = ax^2 + bx + c), "
            "Power (y = ax^b), or Exponential (y = ae^{bx}).",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            x_points = [1.0, 2.0, 3.0, 4.0, 5.0]
            y_points = [1.1, 3.9, 9.2, 16.1, 25.1]
            model_type = "quadratic"
            self.console.print(f"[bold cyan]Example: Quadratic trend[/bold cyan]")
        else:
            x_str = Prompt.ask("Enter x points (space separated)")
            y_str = Prompt.ask("Enter y points (space separated)")
            try:
                x_points = [float(x) for x in x_str.split()]
                y_points = [float(y) for y in y_str.split()]
            except ValueError:
                self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")
                return
            
            model_type = Prompt.ask(
                "Select model type",
                choices=["quadratic", "power", "exponential"],
                default="quadratic"
            )

        solver = CurveFittingSolver()
        try:
            result = solver.solve(x_points=x_points, y_points=y_points, model_type=model_type)
            self.last_steps = solver.get_steps()
            self.formatter.display_least_squares_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Equation: {result.metadata['equation']}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Curve-Fitting")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_euler(self):
        """Run Euler's method solver."""
        self.clear_screen()
        self.display_header("Euler's Method", "First-order ODE Solver")
        
        self.console.print(Panel(
            "Euler's method is the most basic numerical procedure for solving ordinary differential equations (ODEs). "
            "It uses the slope at the current point to predict the next value.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            expression = "x + y"
            x0, y0 = 0.0, 1.0
            h = 0.1
            steps = 10
            self.console.print(f"[bold cyan]Example: dy/dx = x + y, y(0) = 1[/bold cyan]")
        else:
            expression = Prompt.ask("Enter dy/dx = f(x, y) (e.g., x + y)")
            x0 = FloatPrompt.ask("Enter initial x0", default=0.0)
            y0 = FloatPrompt.ask("Enter initial y0", default=1.0)
            h = FloatPrompt.ask("Enter step size h", default=0.1)
            steps = IntPrompt.ask("Enter number of steps", default=10)

        solver = EulerSolver()
        try:
            result = solver.solve(expression=expression, x0=x0, y0=y0, h=h, steps=steps)
            self.last_steps = solver.get_steps()
            self.formatter.display_euler_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Final y value: {result.y_data[-1]:.8f}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Euler")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_rk4(self):
        """Run RK4 method solver."""
        self.clear_screen()
        self.display_header("Runge-Kutta (RK4)", "High-accuracy ODE Solver")
        
        self.console.print(Panel(
            "The fourth-order Runge-Kutta method (RK4) is a highly accurate numerical technique for solving ODEs. "
            "It uses four slope estimates per step to achieve much better precision than Euler's method.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            expression = "x + y"
            x0, y0 = 0.0, 1.0
            h = 0.1
            steps = 10
            self.console.print(f"[bold cyan]Example: dy/dx = x + y, y(0) = 1[/bold cyan]")
        else:
            expression = Prompt.ask("Enter dy/dx = f(x, y) (e.g., x + y)")
            x0 = FloatPrompt.ask("Enter initial x0", default=0.0)
            y0 = FloatPrompt.ask("Enter initial y0", default=1.0)
            h = FloatPrompt.ask("Enter step size h", default=0.1)
            steps = IntPrompt.ask("Enter number of steps", default=10)

        solver = RungeKuttaSolver()
        try:
            result = solver.solve(expression=expression, x0=x0, y0=y0, h=h, steps=steps)
            self.last_steps = solver.get_steps()
            self.formatter.display_rk4_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Final y value: {result.y_data[-1]:.8f}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "RK4")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_least_squares(self):
        """Run Least Squares regression solver."""
        self.clear_screen()
        self.display_header("Least Squares", "Linear Regression (y = mx + c)")
        
        self.console.print(Panel(
            "Least Squares regression finds the best-fitting line through a set of data points by "
            "minimizing the sum of the squares of the vertical deviations from each data point to the line.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            x_points = [1.0, 2.0, 3.0, 4.0, 5.0]
            y_points = [2.1, 3.9, 6.2, 8.1, 10.1]
            self.console.print(f"[bold cyan]Example: Linear trend with noise[/bold cyan]")
            self.console.print(f"X: {x_points}")
            self.console.print(f"Y: {y_points}")
        else:
            x_str = Prompt.ask("Enter x points (space separated)")
            y_str = Prompt.ask("Enter y points (space separated)")
            try:
                x_points = [float(x) for x in x_str.split()]
                y_points = [float(y) for y in y_str.split()]
            except ValueError:
                self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")
                return

        solver = LeastSquaresSolver()
        try:
            result = solver.solve(x_points=x_points, y_points=y_points)
            self.last_steps = solver.get_steps()
            self.formatter.display_least_squares_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Equation: {result.metadata['equation']}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Least-Squares")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def root_finding_menu(self):
        """Root finding submenu."""
        while True:
            self.clear_screen()
            self.display_header("Root Finding", "Solve for f(x) = 0")
            
            options = [
                "Newton-Raphson Method",
                "Simple Iteration Method",
                "Back to Main Menu"
            ]
            self.display_menu_options(options)
            
            choice = IntPrompt.ask(
                "Enter your choice",
                choices=[str(i) for i in range(1, len(options) + 1)],
                show_choices=False
            )

            if choice == 1:
                self.run_newton_raphson()
            elif choice == 2:
                self.run_simple_iteration()
            elif choice == 3:
                break

    def run_newton_raphson(self):
        """Run Newton-Raphson solver."""
        self.clear_screen()
        self.display_header("Newton-Raphson", "Rapid convergence using derivatives")
        
        self.console.print(Panel(
            "Newton-Raphson: A powerful root-finding algorithm that uses derivatives for rapid convergence. "
            "Ideal for smooth functions where the derivative is easily calculated.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            expression = "x**3 - 0.165*x**2 + 3.993e-4"
            initial_guess = 0.05
            tolerance = 1e-6
            max_iterations = 100
            self.console.print(f"[bold cyan]Example: Finding the depth of a floating ball[/bold cyan]")
            self.console.print(f"Function: {expression}")
            self.console.print(f"Initial Guess: {initial_guess}")
        else:
            expression = Prompt.ask("Enter the function f(x) (e.g., x**2 - 2)")
            initial_guess = FloatPrompt.ask("Enter initial guess x0", default=1.0)
            tolerance = FloatPrompt.ask("Enter tolerance", default=1e-6)
            max_iterations = IntPrompt.ask("Enter max iterations", default=100)

        solver = NewtonRaphsonSolver()
        try:
            result = solver.solve(
                expression=expression,
                initial_guess=initial_guess,
                tolerance=tolerance,
                max_iterations=max_iterations
            )
            self.last_steps = solver.get_steps()
            self.formatter.display_newton_raphson_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Root found: {result.metadata['root']:.8f}[/bold green]\n"
                f"Iterations: {result.metadata['iterations']}",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Newton-Raphson")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_simple_iteration(self):
        """Run Simple Iteration solver."""
        self.clear_screen()
        self.display_header("Simple Iteration", "Fixed-point iteration x = g(x)")
        
        self.console.print(Panel(
            "Also known as Fixed-Point Iteration. It transforms f(x)=0 into x=g(x) and iteratively solves for x. "
            "Simple to implement but convergence depends on the derivative of g(x).",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            expression = "cos(x)"
            initial_guess = 0.5
            tolerance = 1e-6
            max_iterations = 100
            self.console.print(f"[bold cyan]Example: Finding intersection of y=x and y=cos(x)[/bold cyan]")
            self.console.print(f"Function g(x): {expression}")
            self.console.print(f"Initial Guess: {initial_guess}")
        else:
            expression = Prompt.ask("Enter the function g(x) for x = g(x) (e.g., cos(x))")
            initial_guess = FloatPrompt.ask("Enter initial guess x0", default=0.0)
            tolerance = FloatPrompt.ask("Enter tolerance", default=1e-6)
            max_iterations = IntPrompt.ask("Enter max iterations", default=100)

        solver = SimpleIterationSolver()
        try:
            result = solver.solve(
                expression=expression,
                initial_guess=initial_guess,
                tolerance=tolerance,
                max_iterations=max_iterations
            )
            self.last_steps = solver.get_steps()
            self.formatter.display_simple_iteration_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Root found: {result.metadata['root']:.8f}[/bold green]\n"
                f"Iterations: {result.metadata['iterations']}",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Simple Iteration")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def network_solver_menu(self):
        """Network solver submenu."""
        while True:
            self.clear_screen()
            self.display_header("Linear Systems", "Solve Ax = b")

            options = [
                "Gauss-Seidel Method",
                "Jacobi Method",
                "Compare Both Methods",
                "Back to Main Menu"
            ]
            self.display_menu_options(options)

            choice = IntPrompt.ask(
                "Enter your choice",
                choices=[str(i) for i in range(1, len(options) + 1)],
                show_choices=False
            )

            if choice == 1:
                self.run_gauss_seidel()
            elif choice == 2:
                self.run_jacobi()
            elif choice == 3:
                self.run_comparison()
            elif choice == 4:
                break

    def run_comparison(self):
        """Run both Jacobi and Gauss-Seidel on the same input and compare."""
        self.clear_screen()
        self.display_header("Method Comparison", "Jacobi vs Gauss-Seidel")

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            matrix = [[4.0, -1.0, -1.0], [-1.0, 4.0, -1.0], [-1.0, -1.0, 4.0]]
            b = [3.0, 2.0, 1.0]
            x0 = [0.0, 0.0, 0.0]
            tol = 1e-6
            max_iter = 100
        else:
            n = IntPrompt.ask("Enter number of equations", default=3)
            matrix = []
            for i in range(n):
                while True:
                    row_str = Prompt.ask(f"Enter coefficients for equation {i+1} (space separated)")
                    try:
                        row = [float(x) for x in row_str.split()]
                        if len(row) != n: continue
                        matrix.append(row)
                        break
                    except ValueError: pass
            
            b_str = Prompt.ask("Enter constants b (space separated)")
            b = [float(x) for x in b_str.split()]
            
            initial_guess_str = Prompt.ask("Enter initial guess (space separated)", default=" ".join(["0"]*n))
            x0 = [float(x) for x in initial_guess_str.split()]
            
            tol = FloatPrompt.ask("Enter tolerance", default=1e-6)
            max_iter = IntPrompt.ask("Enter max iterations", default=100)

        jacobi = JacobiSolver()
        gs = GaussSeidelSolver()

        try:
            res_j = jacobi.solve(A=matrix, b=b, x0=x0, tol=tol, max_iter=max_iter)
            res_gs = gs.solve(A=matrix, b=b, x0=x0, tol=tol, max_iter=max_iter)

            table = Table(title="Solver Comparison", box=box.ROUNDED)
            table.add_column("Metric", style="cyan")
            table.add_column("Jacobi", justify="center")
            table.add_column("Gauss-Seidel", justify="center")
            table.add_column("Winner", justify="center", style="bold green")

            iter_winner = "Gauss-Seidel" if res_gs.metadata['iterations'] < res_j.metadata['iterations'] else "Jacobi"
            if res_gs.metadata['iterations'] == res_j.metadata['iterations']: iter_winner = "Tie"

            table.add_row("Iterations", str(res_j.metadata['iterations']), str(res_gs.metadata['iterations']), iter_winner)
            table.add_row("Final Error", f"{res_j.metadata['final_error']:.4e}", f"{res_gs.metadata['final_error']:.4e}", "N/A")
            table.add_row("Converged", str(res_j.metadata['converged']), str(res_gs.metadata['converged']), "N/A")
            
            self.console.print(table)
            
            self.console.print("\n[bold]Final Solutions:[/bold]")
            self.console.print(f"Jacobi: {res_j.y_data}")
            self.console.print(f"Gauss-Seidel: {res_gs.y_data}")

            # Store Gauss-Seidel steps as primary for export comparison
            self.last_steps = gs.get_steps()
            self.ask_export(self.get_steps_from_result(), "Comparison")

        except Exception as e:
            self.console.print(f"[bold red]Error during comparison: {str(e)}[/bold red]")

        Prompt.ask("\nPress Enter to return to menu")


    def run_gauss_seidel(self):
        """Run Gauss-Seidel solver."""
        self.clear_screen()
        self.display_header("Gauss-Seidel", "Iterative solution for linear systems")
        
        self.console.print(Panel(
            "An iterative method used to solve a system of linear equations. It is particularly efficient "
            "for large, sparse matrices where direct methods are too slow.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            matrix = [
                [4.0, -1.0, -1.0],
                [-1.0, 4.0, -1.0],
                [-1.0, -1.0, 4.0]
            ]
            b = [3.0, 2.0, 1.0]
            x0 = [0.0, 0.0, 0.0]
            tol = 1e-6
            max_iter = 100
            self.console.print(f"[bold cyan]Example: 3x3 System (Truss Analysis)[/bold cyan]")
            self.console.print(f"Matrix A: {matrix}")
            self.console.print(f"Vector b: {b}")
        else:
            n = IntPrompt.ask("Enter number of equations", default=3)
            matrix = []
            for i in range(n):
                while True:
                    row_str = Prompt.ask(f"Enter coefficients for equation {i+1} (space separated)")
                    try:
                        row = [float(x) for x in row_str.split()]
                        if len(row) != n:
                            self.console.print(f"[bold red]Error: Expected {n} coefficients, got {len(row)}[/bold red]")
                            continue
                        matrix.append(row)
                        break
                    except ValueError:
                        self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")
            
            while True:
                b_str = Prompt.ask("Enter constants b (space separated)")
                try:
                    b = [float(x) for x in b_str.split()]
                    if len(b) != n:
                        self.console.print(f"[bold red]Error: Expected {n} constants, got {len(b)}[/bold red]")
                        continue
                    break
                except ValueError:
                    self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")

            initial_guess_str = Prompt.ask("Enter initial guess (space separated)", default=" ".join(["0"]*n))
            try:
                x0 = [float(x) for x in initial_guess_str.split()]
                if len(x0) != n:
                    x0 = [0.0] * n
            except ValueError:
                x0 = [0.0] * n
            
            tol = FloatPrompt.ask("Enter tolerance", default=1e-6)
            max_iter = IntPrompt.ask("Enter max iterations", default=100)

        solver = GaussSeidelSolver()
        try:
            result = solver.solve(
                A=matrix,
                b=b,
                x0=x0,
                tol=tol,
                max_iter=max_iter
            )
            self.last_steps = solver.get_steps()
            self.formatter.display_linear_steps(self.last_steps, method_name="Gauss-Seidel")
            self.console.print(Panel(
                f"[bold green]Solution found: {result.y_data}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Gauss-Seidel")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_jacobi(self):
        """Run Jacobi solver."""
        self.clear_screen()
        self.display_header("Jacobi Method", "Simultaneous iterative solution for linear systems")

        self.console.print(Panel(
            "The Jacobi method solves Ax = b iteratively. Unlike Gauss-Seidel, it computes ALL new values "
            "simultaneously using ONLY values from the previous iteration. This makes it easy to parallelize, "
            "though it typically requires more iterations to converge.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"

        if is_example:
            matrix = [
                [4.0, -1.0, -1.0],
                [-1.0, 4.0, -1.0],
                [-1.0, -1.0, 4.0]
            ]
            b = [3.0, 2.0, 1.0]
            x0 = [0.0, 0.0, 0.0]
            tol = 1e-6
            max_iter = 100
            self.console.print(f"[bold cyan]Example: 3x3 Diagonally Dominant System[/bold cyan]")
            self.console.print(f"Matrix A: {matrix}")
            self.console.print(f"Vector b: {b}")
        else:
            n = IntPrompt.ask("Enter number of equations", default=3)
            matrix = []
            for i in range(n):
                while True:
                    row_str = Prompt.ask(f"Enter coefficients for equation {i+1} (space separated)")
                    try:
                        row = [float(x) for x in row_str.split()]
                        if len(row) != n:
                            self.console.print(f"[bold red]Error: Expected {n} coefficients, got {len(row)}[/bold red]")
                            continue
                        matrix.append(row)
                        break
                    except ValueError:
                        self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")

            while True:
                b_str = Prompt.ask("Enter constants b (space separated)")
                try:
                    b = [float(x) for x in b_str.split()]
                    if len(b) != n:
                        self.console.print(f"[bold red]Error: Expected {n} constants, got {len(b)}[/bold red]")
                        continue
                    break
                except ValueError:
                    self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")

            initial_guess_str = Prompt.ask("Enter initial guess (space separated)", default=" ".join(["0"] * n))
            try:
                x0 = [float(x) for x in initial_guess_str.split()]
                if len(x0) != n:
                    x0 = [0.0] * n
            except ValueError:
                x0 = [0.0] * n

            tol = FloatPrompt.ask("Enter tolerance", default=1e-6)
            max_iter = IntPrompt.ask("Enter max iterations", default=100)

        solver = JacobiSolver()
        try:
            result = solver.solve(
                A=matrix,
                b=b,
                x0=x0,
                tol=tol,
                max_iter=max_iter
            )
            self.last_steps = solver.get_steps()
            self.formatter.display_linear_steps(self.last_steps, method_name="Jacobi")
            self.console.print(Panel(
                f"[bold green]Solution found: {result.y_data}[/bold green]\n"
                f"Iterations: {result.metadata['iterations']} | "
                f"Converged: {result.metadata['converged']}",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Jacobi")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def calculus_menu(self):
        """Calculus submenu."""
        while True:
            self.clear_screen()
            self.display_header("Calculus", "Interpolation, Integration, and Differentiation")
            
            options = [
                "Interpolation (Newton's Divided Difference)",
                "Numerical Integration (Trapezoidal, Simpson's)",
                "Gaussian Quadrature",
                "Numerical Differentiation",
                "Back to Main Menu"
            ]
            self.display_menu_options(options)
            
            choice = IntPrompt.ask(
                "Enter your choice",
                choices=[str(i) for i in range(1, len(options) + 1)],
                show_choices=False
            )

            if choice == 1:
                self.run_interpolation()
            elif choice == 2:
                self.run_integration()
            elif choice == 3:
                self.run_gaussian_quadrature()
            elif choice == 4:
                self.run_numerical_differentiation()
            elif choice == 5:
                break

    def run_gaussian_quadrature(self):
        """Run Gaussian Quadrature solver."""
        self.clear_screen()
        self.display_header("Gaussian Quadrature", "High-precision Integration")
        
        self.console.print(Panel(
            "Gaussian Quadrature is a highly efficient numerical integration method that chooses "
            "optimal sample points (roots of Legendre polynomials) to achieve maximum precision.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            expression = "exp(x**2)"
            a, b = 0.0, 1.0
            n = 3
            self.console.print(f"[bold cyan]Example: Integral of exp(x^2) from 0 to 1[/bold cyan]")
        else:
            expression = Prompt.ask("Enter function f(x) (e.g., x**2 + 1)")
            a = FloatPrompt.ask("Enter lower limit a", default=0.0)
            b = FloatPrompt.ask("Enter upper limit b", default=1.0)
            n = IntPrompt.ask("Enter number of points (2-5)", default=3, choices=["2", "3", "4", "5"])

        solver = GaussianQuadratureSolver()
        try:
            result = solver.solve(expression=expression, a=a, b=b, n=n)
            self.last_steps = solver.get_steps()
            self.formatter.display_integration_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Total Integral: {result.metadata['total_integral']:.8f}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Gaussian-Quadrature")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_numerical_differentiation(self):
        """Run Numerical Differentiation solver."""
        self.clear_screen()
        self.display_header("Numerical Differentiation", "Estimate Derivatives from Data")
        
        self.console.print(Panel(
            "Estimates the derivative of a function at a point using finite difference formulas "
            "(Forward, Backward, or Central).",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            x_points = [0.0, 0.1, 0.2, 0.3, 0.4]
            y_points = [0.0, 0.0998, 0.1987, 0.2955, 0.3894]
            target_x = 0.2
            method = "central"
            self.console.print(f"[bold cyan]Example: Derivative of sin(x) at x=0.2[/bold cyan]")
        else:
            x_str = Prompt.ask("Enter x points (space separated)")
            y_str = Prompt.ask("Enter y points (space separated)")
            try:
                x_points = [float(x) for x in x_str.split()]
                y_points = [float(y) for y in y_str.split()]
            except ValueError:
                self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")
                return
            
            target_x = FloatPrompt.ask("Enter x value to differentiate at")
            method = Prompt.ask(
                "Select differentiation method",
                choices=["forward", "backward", "central"],
                default="central"
            )

        solver = NumericalDifferentiationSolver()
        try:
            result = solver.solve(x_points=x_points, y_points=y_points, target_x=target_x, method=method)
            self.last_steps = solver.get_steps()
            # Reusing interpolation steps display as it's similar (table of values)
            self.formatter.display_interpolation_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Derivative at x={target_x}: {result.metadata['derivative']:.8f}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Differentiation")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_interpolation(self):
        """Run Interpolation solver."""
        self.clear_screen()
        self.display_header("Interpolation", "Newton's Divided Difference")
        
        self.console.print(Panel(
            "Uses Newton's Divided Difference to find a polynomial that passes through a set of data points. "
            "Useful for estimating values between known data points in engineering tables.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            x_points = [0.0, 10.0, 20.0, 30.0, 40.0]
            y_points = [4.217, 4.192, 4.181, 4.178, 4.178]
            target_x = [25.0]
            self.console.print(f"[bold cyan]Example: Specific heat of water vs Temperature[/bold cyan]")
            self.console.print(f"X (Temp): {x_points}")
            self.console.print(f"Y (Heat): {y_points}")
            self.console.print(f"Target X: {target_x}")
        else:
            x_str = Prompt.ask("Enter x points (space separated)")
            y_str = Prompt.ask("Enter y points (space separated)")
            try:
                x_points = [float(x) for x in x_str.split()]
                y_points = [float(y) for y in y_str.split()]
            except ValueError:
                self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")
                return
            
            target_x_str = Prompt.ask("Enter target x value(s) to interpolate (optional, space separated)", default="")
            try:
                target_x = [float(x) for x in target_x_str.split()] if target_x_str else None
            except ValueError:
                target_x = None

        solver = InterpolationSolver()
        try:
            result = solver.solve(
                x_points=x_points,
                y_points=y_points,
                target_x=target_x
            )
            self.last_steps = solver.get_steps()
            self.formatter.display_interpolation_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Interpolated values: {result.y_data}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Interpolation")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")

    def run_integration(self):
        """Run Integration solver."""
        self.clear_screen()
        self.display_header("Integration", "Numerical Quadrature")
        
        self.console.print(Panel(
            "Numerical integration using Trapezoidal or Simpson's rules. Essential for calculating areas, "
            "volumes, or total work when the function is only known at discrete points.",
            title="[bold]Method Description[/bold]",
            border_style="blue",
            padding=(1, 1)
        ))

        is_example = Prompt.ask("Load engineering example? (y/n)", choices=["y", "n"], default="n") == "y"
        
        if is_example:
            x_points = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0]
            y_points = [0.0, 227.0, 362.0, 517.0, 602.0, 756.0, 901.0]
            method = "simpson13"
            self.console.print(f"[bold cyan]Example: Velocity of a rocket over time[/bold cyan]")
            self.console.print(f"Time (s): {x_points}")
            self.console.print(f"Velocity (m/s): {y_points}")
            self.console.print(f"Method: {method}")
        else:
            x_str = Prompt.ask("Enter x points (space separated)")
            y_str = Prompt.ask("Enter y points (space separated)")
            try:
                x_points = [float(x) for x in x_str.split()]
                y_points = [float(y) for y in y_str.split()]
            except ValueError:
                self.console.print("[bold red]Error: Please enter valid numbers.[/bold red]")
                return
            
            method = Prompt.ask(
                "Select integration method",
                choices=["trapezoidal", "simpson13", "simpson38"],
                default="trapezoidal"
            )

        solver = IntegrationSolver()
        try:
            result = solver.solve(
                x_points=x_points,
                y_points=y_points,
                method=method
            )
            self.last_steps = solver.get_steps()
            self.formatter.display_integration_steps(self.last_steps)
            self.console.print(Panel(
                f"[bold green]Total Integral: {result.metadata['total_integral']:.8f}[/bold green]",
                title="Result",
                border_style="green"
            ))
            self.ask_export(self.get_steps_from_result(), "Integration")
        except Exception as e:
            self.console.print(f"[bold red]Error: {str(e)}[/bold red]")
        
        Prompt.ask("\nPress Enter to return to menu")


def launch_cli():
    """Launch the CLI application."""
    cli = NumericalCLI()
    cli.main_menu()


if __name__ == "__main__":
    launch_cli()
