import customtkinter as ctk
import tkinter as tk

class HelpProvider:
    """Provides help content and UI components for the NUM-CORE GUI."""
    
    HELP_CONTENT = {
        "root_finder": {
            "title": "Newton-Raphson Method",
            "description": "An iterative method to find roots of a real-valued function f(x) = 0.",
            "details": "It uses the formula: x_{n+1} = x_n - f(x_n) / f'(x_n).\n\n"
                       "Requirements:\n"
                       "- Function must be differentiable.\n"
                       "- Initial guess should be close to the actual root."
        },
        "network_solver": {
            "title": "Gauss-Seidel Method",
            "description": "An iterative method used to solve a linear system of equations Ax = b.",
            "details": "It is particularly useful for large, sparse matrices.\n\n"
                       "Diagonal Dominance:\n"
                       "For convergence, the matrix A should ideally be strictly diagonally dominant: "
                       "|a_ii| > sum_{j != i} |a_ij| for all i."
        },
        "calculus": {
            "title": "Numerical Calculus Engine",
            "description": "Tools for numerical differentiation and integration.",
            "details": "Integration: Uses Simpson's 1/3 rule for high accuracy with parabolic interpolation.\n"
                       "Differentiation: Uses central difference formulas for O(h^2) error reduction."
        },
        "diagonal_dominance": {
            "title": "Diagonal Dominance",
            "description": "A matrix is diagonally dominant if the absolute value of the diagonal element "
                           "is greater than or equal to the sum of the absolute values of the other elements in that row.",
            "details": "Strict diagonal dominance ensures that iterative methods like Gauss-Seidel will converge."
        }
    }

    @staticmethod
    def show_help(key):
        """Displays a help dialog for the given key."""
        content = HelpProvider.HELP_CONTENT.get(key)
        if not content:
            return

        dialog = ctk.CTkToplevel()
        dialog.title(f"Help: {content['title']}")
        dialog.geometry("450x350")
        dialog.attributes("-topmost", True)

        label_title = ctk.CTkLabel(dialog, text=content['title'], font=ctk.CTkFont(size=16, weight="bold"))
        label_title.pack(pady=(20, 10), padx=20)

        # Use a scrollable frame or text widget for the content
        text_area = tk.Text(dialog, wrap="word", font=("Arial", 11), bg="#2b2b2b", fg="white", bd=0, highlightthickness=0, padx=10, pady=10)
        text_area.insert("1.0", f"{content['description']}\n\n{content['details']}")
        text_area.configure(state="disabled")
        text_area.pack(pady=10, padx=20, fill="both", expand=True)

        close_button = ctk.CTkButton(dialog, text="Close", command=dialog.destroy)
        close_button.pack(pady=(0, 20))

    @staticmethod
    def create_help_button(master, key, **kwargs):
        """Creates a small help button that triggers a help dialog."""
        button_kwargs = {
            "text": "?", 
            "width": 20, 
            "height": 20, 
            "corner_radius": 10,
            "fg_color": "gray30",
            "hover_color": "gray50",
            "font": ctk.CTkFont(size=10, weight="bold"),
            "command": lambda: HelpProvider.show_help(key)
        }
        button_kwargs.update(kwargs)
        return ctk.CTkButton(master, **button_kwargs)
