import customtkinter as ctk
from typing import Optional
from numcore_engine.models import ComparisonResult, NumericalData
from numcore_gui import theme


class SmartSolverPanel(ctk.CTkFrame):
    """
    Inline frame to display Smart Solver comparison results within a chapter page.
    Shows recommendation card and performance table, or diagnostic panel on all-diverge.
    """

    def __init__(self, master, comparison_result=None, **kwargs):
        super().__init__(master, fg_color=theme.get_bg_color(), border_color=theme.get_border_color(), border_width=1, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Recommendation / Diagnostic header
        self.header_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=theme.get_panel_color(), border_color=theme.get_border_color(), border_width=1)
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.rec_title = ctk.CTkLabel(
            self.header_frame,
            text="Smart Recommendation",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme.SUCCESS,
        )
        self.rec_title.pack(padx=15, pady=(12, 4), anchor="w")

        self.rec_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            wraplength=700,
            justify="left",
            font=ctk.CTkFont(size=12),
        )
        self.rec_label.pack(padx=15, pady=(0, 12), anchor="w")

        # Comparison table
        self.table_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Performance Comparison",
            corner_radius=8,
            fg_color=theme.get_bg_color(),
            label_fg_color=theme.get_panel_color(),
            height=200,
        )
        self.table_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.table_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        if comparison_result is not None:
            self.populate(comparison_result)

    def populate(self, result: ComparisonResult):
        """Fill the panel with a ComparisonResult."""
        # Clear table
        for w in self.table_frame.winfo_children():
            w.destroy()

        if result.all_diverged:
            self.rec_title.configure(text="All Methods Diverged", text_color=theme.WARN)
            self.rec_label.configure(text=result.recommendation)
            self._render_diagnostic_rows(result)
        else:
            self.rec_title.configure(text="Smart Recommendation", text_color=theme.SUCCESS)
            self.rec_label.configure(text=result.recommendation)
            self._render_comparison_rows(result)

    def _render_comparison_rows(self, result: ComparisonResult):
        headers = ["Method", "Time (ms)", "Iterations", "Result", "Status"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_frame, text=h, font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=i, padx=8, pady=8, sticky="nsew"
            )

        for r_idx, res in enumerate(result.results):
            is_best = res.title == result.best_method
            diverged = res.metadata.get("diverged", False)
            bg = theme.ACCENT_BLUE if is_best else ("transparent" if not diverged else "transparent")
            text_col = theme.ERROR if diverged else ("white" if not is_best else "black")

            ctk.CTkLabel(self.table_frame, text=res.title, fg_color=bg, text_color=text_col).grid(
                row=r_idx + 1, column=0, padx=5, pady=4, sticky="ew"
            )
            ctk.CTkLabel(self.table_frame, text=f"{res.computation_time_ms:.2f}").grid(
                row=r_idx + 1, column=1, padx=5, pady=4
            )
            ctk.CTkLabel(self.table_frame, text=str(res.metadata.get("iterations", "--"))).grid(
                row=r_idx + 1, column=2, padx=5, pady=4
            )

            val = "--"
            for key in ("root", "total_integral", "interpolated_y"):
                if key in res.metadata and isinstance(res.metadata[key], (int, float)):
                    val = f"{res.metadata[key]:.6f}"
                    break
            if diverged:
                val = "Diverged"
            ctk.CTkLabel(self.table_frame, text=val).grid(row=r_idx + 1, column=3, padx=5, pady=4)

            status = "BEST" if is_best else ("DIVERGED" if diverged else "OK")
            status_color = theme.SUCCESS if is_best else (theme.ERROR if diverged else "gray")
            ctk.CTkLabel(self.table_frame, text=status, text_color=status_color).grid(
                row=r_idx + 1, column=4, padx=5, pady=4
            )

    def _render_diagnostic_rows(self, result: ComparisonResult):
        headers = ["Method", "Reason"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.table_frame, text=h, font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=i, padx=8, pady=8, sticky="nsew"
            )
        for r_idx, res in enumerate(result.results):
            reason = res.metadata.get("error_reason", "Diverged — check initial values or parameters")
            ctk.CTkLabel(self.table_frame, text=res.title, text_color=theme.WARN).grid(
                row=r_idx + 1, column=0, padx=5, pady=4, sticky="ew"
            )
            ctk.CTkLabel(self.table_frame, text=reason, wraplength=500, justify="left").grid(
                row=r_idx + 1, column=1, padx=5, pady=4, sticky="ew"
            )
