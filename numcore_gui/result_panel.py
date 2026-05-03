import customtkinter as ctk
from typing import List, Dict, Any, Optional
from numcore_engine.models import NumericalStep, SimulationData
from numcore_gui.theme import BLACK, PANEL, BORDER

class ResultPanel(ctk.CTkFrame):
    """
    A reusable GUI component to display numerical results and methodology tables.
    Matches the 'Lecturer Methodology Tables' requirement.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BLACK, border_color=BORDER, border_width=1, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Table takes most space
        
        # Summary Frame
        self.summary_frame = ctk.CTkFrame(self, corner_radius=5, fg_color=PANEL)
        self.summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.summary_label = ctk.CTkLabel(
            self.summary_frame, 
            text="No results yet. Execute a solver to see data.", 
            justify="left",
            font=ctk.CTkFont(size=12)
        )
        self.summary_label.pack(padx=15, pady=15, fill="x")
        
        # Table Frame
        self.table_frame = ctk.CTkScrollableFrame(
            self, 
            label_text="Methodology Steps / Table", 
            corner_radius=5,
            fg_color=BLACK,
            label_fg_color=PANEL
        )
        self.table_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        
    def update_result(self, data: SimulationData, steps: List[NumericalStep]):
        """Update the panel with new simulation data and steps."""
        # Update summary
        summary_text = f"Method: {data.title}\n"
        
        if "root" in data.metadata:
            summary_text += f"Root: {data.metadata['root']:.8f}\n"
        if "total_integral" in data.metadata:
            summary_text += f"Integral: {data.metadata['total_integral']:.8f}\n"
        if "iterations" in data.metadata:
            summary_text += f"Iterations: {data.metadata['iterations']}\n"
        if "h" in data.metadata:
            h = data.metadata['h']
            summary_text += f"h: {h:.6f}\n" if isinstance(h, float) else f"h: {h}\n"
        if "weighted_sum_str" in data.metadata:
            summary_text += f"\nFormula Breakdown:\n{data.metadata['weighted_sum_str']}\n"
        if "polynomial_str" in data.metadata:
            summary_text += f"\nPolynomial:\n{data.metadata['polynomial_str']}\n"
        if "target_x" in data.metadata and data.metadata.get("target_x") is not None:
            y_val = data.metadata.get('interpolated_y')
            if y_val is not None:
                summary_text += f"\nInterpolated value at x={data.metadata['target_x']}: {y_val:.8f}\n"
            
        self.summary_label.configure(text=summary_text)
        
        # Update table
        self._clear_table()
        if not steps:
            return
            
        # Determine headers from all steps
        all_keys = set()
        for s in steps:
            all_keys.update(s.details.keys())
        
        # Preferred order for common keys
        preferred = ["x", "y", "a", "b", "f(a)", "f(b)", "c", "f(c)", "x0", "x1", "f(x0)", "f(x1)", "x2", "weight", "weighted_y"]
        
        # Handle difference table keys (diff_1, diff_2, dd_1, dd_2, etc.)
        diff_keys = sorted([k for k in all_keys if k.startswith("diff_") or k.startswith("dd_")], 
                          key=lambda x: int(x.split("_")[1]))
        
        detail_keys = [k for k in preferred if k in all_keys]
        detail_keys += diff_keys
        # Add remaining keys
        detail_keys += sorted([k for k in all_keys if k not in preferred and k not in diff_keys])

        # Build headers list
        headers = ["Step"] + detail_keys
        
        # Only add Value/Error if they are meaningful
        has_value = any(s.value != 0 for s in steps)
        has_error = any(s.error is not None for s in steps)
        
        if has_value: headers.append("Value")
        if has_error: headers.append("Error")
        
        # Create header labels
        for i, h in enumerate(headers):
            # Map internal keys to lecturer-friendly names
            display_name = h
            if h == "x": display_name = "x_i"
            elif h == "y": display_name = "y_i"
            elif h.startswith("diff_"): display_name = f"Δ^{h.split('_')[1]}y"
            elif h.startswith("dd_"): display_name = f"Order {h.split('_')[1]}"
            
            lbl = ctk.CTkLabel(self.table_frame, text=display_name, font=ctk.CTkFont(weight="bold", size=11))
            lbl.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            
        # Create data rows
        for r_idx, step in enumerate(steps):
            # Step index
            ctk.CTkLabel(self.table_frame, text=str(step.step_idx), font=ctk.CTkFont(size=11)).grid(row=r_idx+1, column=0, padx=10, pady=2)
            
            # Details
            for c_idx, key in enumerate(detail_keys):
                val = step.details.get(key, "")
                text = f"{val:.6f}" if isinstance(val, float) else str(val)
                ctk.CTkLabel(self.table_frame, text=text, font=ctk.CTkFont(size=11)).grid(row=r_idx+1, column=c_idx+1, padx=10, pady=2)
            
            # Value and Error
            curr_col = len(detail_keys) + 1
            if has_value:
                ctk.CTkLabel(self.table_frame, text=f"{step.value:.6f}", font=ctk.CTkFont(size=11)).grid(row=r_idx+1, column=curr_col, padx=10, pady=2)
                curr_col += 1
            if has_error:
                err_text = f"{step.error:.2e}" if step.error is not None else "--"
                ctk.CTkLabel(self.table_frame, text=err_text, font=ctk.CTkFont(size=11)).grid(row=r_idx+1, column=curr_col, padx=10, pady=2)

    def _clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
            
    def clear(self):
        """Reset the panel to its initial state."""
        self.summary_label.configure(text="No results yet. Execute a solver to see data.")
        self._clear_table()
