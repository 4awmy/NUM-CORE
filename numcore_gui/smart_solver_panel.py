import customtkinter as ctk
from typing import List, Dict, Any, Optional

class SmartSolverPanel(ctk.CTkFrame):
    """
    A panel that displays comparison results between different numerical methods.
    It includes a recommendation card and a detailed comparison table.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        # Recommendation Card
        self.recommendation_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("gray80", "gray20"))
        self.recommendation_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.recommendation_frame.grid_columnconfigure(0, weight=1)
        
        self.rec_title = ctk.CTkLabel(
            self.recommendation_frame, 
            text="Recommended Method", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.rec_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.rec_method_label = ctk.CTkLabel(
            self.recommendation_frame, 
            text="Method: N/A", 
            font=ctk.CTkFont(size=16, weight="bold", color="#4CAF50")
        )
        self.rec_method_label.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        
        self.rec_details_label = ctk.CTkLabel(
            self.recommendation_frame, 
            text="Iterations: 0 | Error: 0", 
            font=ctk.CTkFont(size=12)
        )
        self.rec_details_label.grid(row=2, column=0, padx=10, pady=2, sticky="w")
        
        self.rec_reason_label = ctk.CTkLabel(
            self.recommendation_frame, 
            text="Reason: N/A", 
            font=ctk.CTkFont(size=11, slant="italic"),
            wraplength=400,
            justify="left"
        )
        self.rec_reason_label.grid(row=3, column=0, padx=10, pady=(2, 10), sticky="w")

        # Comparison Table
        self.table_frame = ctk.CTkFrame(self, corner_radius=10)
        self.table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.table_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self._create_table_headers()
        
        # Diagnostic Panel (Hidden by default)
        self.diagnostic_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFF9C4") # Light yellow
        self.diagnostic_label = ctk.CTkLabel(
            self.diagnostic_frame, 
            text="All methods diverged!", 
            text_color="#FBC02D", # Darker yellow/orange
            font=ctk.CTkFont(weight="bold")
        )
        self.diagnostic_label.pack(padx=10, pady=10)

    def _create_table_headers(self):
        headers = ["Method", "Status", "Iters", "Final Error"]
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=header, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=i, padx=5, pady=5)

    def populate(self, results: List[Dict[str, Any]]):
        """
        Populates the panel with comparison results.
        
        results: List of dicts with keys: 
                 'method', 'status', 'iterations', 'error', 'diverged', 'reason', 'root'
        """
        # Clear previous table rows
        for widget in self.table_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        
        if not results:
            return

        # Hide diagnostic frame by default
        self.diagnostic_frame.grid_forget()

        # Find best method (converged, then minimum iterations)
        converged_results = [r for r in results if not r['diverged']]
        
        if not converged_results:
            self.rec_method_label.configure(text="Method: NONE", text_color="#f44336")
            self.rec_details_label.configure(text="All methods failed to converge.")
            self.rec_reason_label.configure(text="Try adjusting initial guesses or increasing max iterations.")
            
            # Show diagnostic panel
            self.diagnostic_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
            diag_text = "Diagnostics:\n" + "\n".join([f"- {r['method']}: {r.get('reason', 'Diverged')}" for r in results])
            self.diagnostic_label.configure(text=diag_text)
        else:
            best = min(converged_results, key=lambda x: x['iterations'])
            self.rec_method_label.configure(text=f"Method: {best['method']}", text_color="#4CAF50")
            self.rec_details_label.configure(text=f"Iterations: {best['iterations']} | Error: {best['error']:.2e}")
            self.rec_reason_label.configure(text=f"Reason: {best.get('reason', 'Fastest convergence with acceptable error.')}")

        # Populate table
        for i, res in enumerate(results):
            row = i + 1
            status_color = "#4CAF50" if not res['diverged'] else "#f44336"
            status_text = "Converged" if not res['diverged'] else "Diverged"
            
            ctk.CTkLabel(self.table_frame, text=res['method']).grid(row=row, column=0, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=status_text, text_color=status_color).grid(row=row, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=str(res['iterations'])).grid(row=row, column=2, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=f"{res['error']:.2e}").grid(row=row, column=3, padx=5, pady=2)
