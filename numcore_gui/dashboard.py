import customtkinter as ctk
import tkinter as tk
from numcore_gui.pages.root_finder_page import RootFinderPage
from numcore_gui.pages.network_solver_page import NetworkSolverPage
from numcore_gui.pages.calculus_page import CalculusPage
from numcore_gui.pages.interpolation_page import InterpolationPage
from numcore_gui.pages.chapter_1_app import Chapter1AppPage
from numcore_gui.pages.chapter_2_app import Chapter2AppPage
from numcore_gui.pages.chapter_3_app import Chapter3AppPage
from numcore_gui.pages.chapter_4_app import Chapter4AppPage
from numcore_gui.help_system import HelpProvider
from numcore_gui.theme import BLACK, PANEL, BORDER

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NUM-CORE | Numerical Methods")
        self.geometry("1280x800")
        self.configure(fg_color=BLACK)
        ctk.set_appearance_mode("dark")

        # Configure grid layout (2x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0) # Status bar

        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=PANEL)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(11, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="NUM-CORE", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Solver Pages Section
        self.solver_label = ctk.CTkLabel(self.sidebar_frame, text="Solver Pages (Ch 1-4)", font=ctk.CTkFont(size=12, weight="bold"))
        self.solver_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")

        self.ch1_solver_btn = ctk.CTkButton(self.sidebar_frame, text="Ch 1: Root Finding", command=self.show_root_finder)
        self.ch1_solver_btn.grid(row=2, column=0, padx=20, pady=5)
        
        self.ch2_solver_btn = ctk.CTkButton(self.sidebar_frame, text="Ch 2: Linear Systems", command=self.show_network_solver)
        self.ch2_solver_btn.grid(row=3, column=0, padx=20, pady=5)

        self.ch3_solver_btn = ctk.CTkButton(self.sidebar_frame, text="Ch 3: Numerical Calculus", command=self.show_calculus)
        self.ch3_solver_btn.grid(row=4, column=0, padx=20, pady=5)

        self.ch4_solver_btn = ctk.CTkButton(self.sidebar_frame, text="Ch 4: Interpolation", command=self.show_interpolation)
        self.ch4_solver_btn.grid(row=5, column=0, padx=20, pady=5)

        # Scientific Applications Section
        self.apps_label = ctk.CTkLabel(self.sidebar_frame, text="Scientific Applications", font=ctk.CTkFont(size=12, weight="bold"))
        self.apps_label.grid(row=6, column=0, padx=20, pady=(20, 5), sticky="w")

        self.ch1_app_btn = ctk.CTkButton(self.sidebar_frame, text="Ch 1: Beam Stress", command=self.show_ch1_app)
        self.ch1_app_btn.grid(row=7, column=0, padx=20, pady=5)

        self.ch2_app_btn = ctk.CTkButton(self.sidebar_frame, text="Ch 2: Circuit Analysis", command=self.show_ch2_app)
        self.ch2_app_btn.grid(row=8, column=0, padx=20, pady=5)

        self.ch3_app_btn = ctk.CTkButton(self.sidebar_frame, text="Ch 3: Data Fitting", command=self.show_ch3_app)
        self.ch3_app_btn.grid(row=9, column=0, padx=20, pady=5)

        self.ch4_app_btn = ctk.CTkButton(self.sidebar_frame, text="Ch 4: Work Done", command=self.show_ch4_app)
        self.ch4_app_btn.grid(row=10, column=0, padx=20, pady=5)

        # Help button in sidebar
        self.help_info_label = ctk.CTkLabel(self.sidebar_frame, text="System Help:", anchor="w")
        self.help_info_label.grid(row=11, column=0, padx=20, pady=(20, 0), sticky="s")
        self.help_button = HelpProvider.create_help_button(self.sidebar_frame, "calculus", text="Open Help Center", width=160)
        self.help_button.grid(row=12, column=0, padx=20, pady=(5, 10), sticky="s")

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=13, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=14, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("Dark")

        # Main content frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BLACK)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Status bar
        self.status_bar = ctk.CTkFrame(self, height=25, corner_radius=0, fg_color=PANEL)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_label = ctk.CTkLabel(self.status_bar, text="System Ready", font=ctk.CTkFont(size=10))
        self.status_label.pack(side="left", padx=20)


        # Initialize pages
        self.pages = {}
        self.pages["root_finder"] = RootFinderPage(self.main_frame)
        self.pages["network_solver"] = NetworkSolverPage(self.main_frame)
        self.pages["calculus"] = CalculusPage(self.main_frame)
        self.pages["interpolation"] = InterpolationPage(self.main_frame)
        self.pages["ch1_app"] = Chapter1AppPage(self.main_frame)
        self.pages["ch2_app"] = Chapter2AppPage(self.main_frame)
        self.pages["ch3_app"] = Chapter3AppPage(self.main_frame)
        self.pages["ch4_app"] = Chapter4AppPage(self.main_frame)

        # Show default page
        self.show_root_finder()

    def show_root_finder(self):
        self.select_page("root_finder")
        self.status_label.configure(text="Active: Ch 1 - Root Finding")

    def show_network_solver(self):
        self.select_page("network_solver")
        self.status_label.configure(text="Active: Ch 2 - Linear Systems")

    def show_calculus(self):
        self.select_page("calculus")
        self.status_label.configure(text="Active: Ch 3 - Numerical Calculus")

    def show_interpolation(self):
        self.select_page("interpolation")
        self.status_label.configure(text="Active: Ch 4 - Interpolation")

    def show_ch1_app(self):
        self.select_page("ch1_app")
        self.status_label.configure(text="Active: Ch 1 App - Beam Stress")

    def show_ch2_app(self):
        self.select_page("ch2_app")
        self.status_label.configure(text="Active: Ch 2 App - Circuit Analysis")

    def show_ch3_app(self):
        self.select_page("ch3_app")
        self.status_label.configure(text="Active: Ch 3 App - Data Fitting")

    def show_ch4_app(self):
        self.select_page("ch4_app")
        self.status_label.configure(text="Active: Ch 4 App - Work Done")

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
