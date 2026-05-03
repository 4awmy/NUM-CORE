from typing import Callable, List, Optional, Union
import re
import sympy


class SymbolicParser:
    @staticmethod
    def normalize(expression: str) -> str:
        """
        Normalize a mathematical expression string for SymPy compatibility.

        Args:
            expression: The raw input expression.

        Returns:
            A normalized string expression.
        """
        if not expression:
            return ""

        # Replace common notation with SymPy-compatible notation
        # ^ -> **
        normalized = expression.replace("^", "**")

        # ln -> log (using word boundaries to avoid replacing inside variable names)
        normalized = re.sub(r"\bln\b", "log", normalized)

        return normalized

    @staticmethod
    def validate(expression: str, allowed_variables: Optional[List[str]] = None) -> bool:
        """
        Validate if an expression is mathematically sound and parseable.

        Args:
            expression: The expression string to validate.
            allowed_variables: Optional list of allowed variable names.

        Returns:
            True if valid, False otherwise.
        """
        if not expression or not expression.strip():
            return False

        try:
            normalized = SymbolicParser.normalize(expression)
            expr = sympy.sympify(normalized)

            if allowed_variables is not None:
                symbols = [str(s) for s in expr.free_symbols]
                for s in symbols:
                    if s not in allowed_variables:
                        return False

            return True
        except (sympy.SympifyError, TypeError, SyntaxError, ValueError):
            return False

    @staticmethod
    def get_symbols(expression: str) -> List[str]:
        """
        Extract all variable symbols from an expression.

        Args:
            expression: The expression string.

        Returns:
            A list of symbol names as strings.
        """
        if not expression or not expression.strip():
            return []

        try:
            normalized = SymbolicParser.normalize(expression)
            expr = sympy.sympify(normalized)
            return sorted([str(s) for s in expr.free_symbols])
        except (sympy.SympifyError, TypeError, SyntaxError, ValueError):
            return []

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

        normalized = SymbolicParser.normalize(expression)
        symbols = [sympy.Symbol(var) for var in variables]
        expr = sympy.sympify(normalized)
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
        normalized = SymbolicParser.normalize(expression)
        sym_var = sympy.Symbol(variable)
        expr = sympy.sympify(normalized)
        derivative = sympy.diff(expr, sym_var, order)
        return str(derivative)
