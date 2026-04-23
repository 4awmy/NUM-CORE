import customtkinter as ctk
import tkinter as tk
from numcore_gui.pages.root_finder_page import RootFinderPage
from numcore_gui.pages.network_solver_page import NetworkSolverPage
from numcore_gui.pages.calculus_page import CalculusPage
from numcore_gui.help_system import HelpProvider

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NUM-CORE | Mission Control")
        self.geometry("1100x700")

        # Configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="NUM-CORE", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.mission_label = ctk.CTkLabel(self.sidebar_frame, text="Missions", font=ctk.CTkFont(size=12, slant="italic"))
        self.mission_label.grid(row=1, column=0, padx=20, pady=(10, 0))

        self.root_finder_button = ctk.CTkButton(self.sidebar_frame, text="Beam Stress", command=self.show_root_finder)
        self.root_finder_button.grid(row=2, column=0, padx=20, pady=10)

        self.network_solver_button = ctk.CTkButton(self.sidebar_frame, text="Circuit Analysis", command=self.show_network_solver)
        self.network_solver_button.grid(row=3, column=0, padx=20, pady=10)

        self.calculus_button = ctk.CTkButton(self.sidebar_frame, text="Calculus Engine", command=self.show_calculus)
        self.calculus_button.grid(row=4, column=0, padx=20, pady=10)

        # Help button in sidebar
        self.help_info_label = ctk.CTkLabel(self.sidebar_frame, text="System Help:", anchor="w")
        self.help_info_label.grid(row=5, column=0, padx=20, pady=(20, 0), sticky="s")
        self.help_button = HelpProvider.create_help_button(self.sidebar_frame, "calculus", text="Open Help Center", width=160)
        self.help_button.grid(row=6, column=0, padx=20, pady=(5, 10), sticky="s")

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Main content frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Initialize pages
        self.pages = {}
        self.pages["root_finder"] = RootFinderPage(self.main_frame)
        self.pages["network_solver"] = NetworkSolverPage(self.main_frame)
        self.pages["calculus"] = CalculusPage(self.main_frame)

        # Show default page
        self.show_root_finder()

    def show_root_finder(self):
        self.select_page("root_finder")

    def show_network_solver(self):
        self.select_page("network_solver")

    def show_calculus(self):
        self.select_page("calculus")

    def select_page(self, page_name):
        # Hide all pages
        for page in self.pages.values():
            page.grid_forget()
        
        # Show selected page
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
