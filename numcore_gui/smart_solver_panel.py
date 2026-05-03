import customtkinter as ctk
from typing import List, Dict, Any, Optional
from numcore_engine.models import ComparisonResult, NumericalData
from numcore_gui.theme import BLACK, PANEL, BORDER

class SmartSolverPanel(ctk.CTkToplevel):
    """
    A popup window to display comparison results between multiple solvers.
    """
    def __init__(self, master, comparison_result: ComparisonResult, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("Smart Solver Comparison")
        self.geometry("700x500")
        self.configure(fg_color=BLACK)
        
        # Make it modal-like
        self.after(10, self.lift)
        self.focus_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Recommendation Header
        self.header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=PANEL, border_color=BORDER, border_width=1)
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.rec_title = ctk.CTkLabel(
            self.header_frame, 
            text="Smart Recommendation", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50" # Greenish
        )
        self.rec_title.pack(padx=20, pady=(15, 5), anchor="w")
        
        self.rec_label = ctk.CTkLabel(
            self.header_frame, 
            text=comparison_result.recommendation,
            wraplength=600,
            justify="left",
            font=ctk.CTkFont(size=13)
        )
        self.rec_label.pack(padx=20, pady=(0, 15), anchor="w")
        
        # Comparison Table
        self.table_frame = ctk.CTkScrollableFrame(
            self, 
            label_text="Performance Comparison", 
            corner_radius=10,
            fg_color=BLACK,
            label_fg_color=PANEL
        )
        self.table_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.table_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Headers
        headers = ["Method", "Time (ms)", "Iterations", "Result"]
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=h, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
        # Data Rows
        for r_idx, res in enumerate(comparison_result.results):
            # Highlight best method
            is_best = res.title == comparison_result.best_method
            bg_color = "#2E7D32" if is_best else "transparent"
            
            # Method Name
            ctk.CTkLabel(self.table_frame, text=res.title, fg_color=bg_color).grid(row=r_idx+1, column=0, padx=5, pady=5, sticky="ew")
            
            # Time
            ctk.CTkLabel(self.table_frame, text=f"{res.computation_time_ms:.2f}").grid(row=r_idx+1, column=1, padx=5, pady=5)
            
            # Iterations
            iters = res.metadata.get("iterations", "--")
            ctk.CTkLabel(self.table_frame, text=str(iters)).grid(row=r_idx+1, column=2, padx=5, pady=5)
            
            # Result (Root or value)
            result_val = "--"
            if "root" in res.metadata:
                result_val = f"{res.metadata['root']:.6f}"
            elif "total_integral" in res.metadata:
                result_val = f"{res.metadata['total_integral']:.6f}"
            elif "interpolated_y" in res.metadata:
                result_val = f"{res.metadata['interpolated_y']:.6f}"
                
            if res.metadata.get("diverged", False):
                result_val = "Diverged"
                
            ctk.CTkLabel(self.table_frame, text=result_val).grid(row=r_idx+1, column=3, padx=5, pady=5)

        # Close Button
        self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.grid(row=2, column=0, padx=20, pady=20)
