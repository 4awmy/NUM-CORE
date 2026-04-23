from typing import Callable, List, Optional, Union

import sympy


class SymbolicParser:
    @staticmethod
    def parse_expression(
        expression: str, variables: Union[str, List[str]] = "x"
    ) -> Callable[..., float]:
        """
        Parse a string expression into a callable Python function.

        Args:
            expression: The string expression to parse (e.g., 'x**2 + 5').
            variables: The variable(s) in the expression. Defaults to 'x'.

        Returns:
            A callable function that evaluates the expression.
        """
        if isinstance(variables, str):
            variables = [variables]

        symbols = [sympy.Symbol(var) for var in variables]
        expr = sympy.sympify(expression)
        return sympy.lambdify(symbols, expr, modules=["numpy"])

    @staticmethod
    def get_derivative(
        expression: str, variable: str = "x", order: int = 1
    ) -> str:
        """
        Calculate the derivative of a string expression.

        Args:
            expression: The string expression to differentiate.
            variable: The variable to differentiate with respect to.
            order: The order of the derivative.

        Returns:
            The string representation of the derivative.
        """
        sym_var = sympy.Symbol(variable)
        expr = sympy.sympify(expression)
        derivative = sympy.diff(expr, sym_var, order)
        return str(derivative)
