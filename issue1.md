## Problem

The current GUI uses a confusing "Mission Control" space theme ("Mission: Beam Stress",
"Analyze Circuit") that is unrelated to the numerical methods content. Pages use
hardcoded mock data. Layout is too cramped.

## Tasks

- [x] Remove all "Mission" labels — rename to proper method names
- [x] Sidebar: "Root Finding", "Linear Systems", "Calculus"
- [x] Default to Dark theme
- [x] Increase default window to 1280x800
- [x] Add method selector dropdown per page (e.g., Newton-Raphson vs Simple Iteration)
- [x] Add tolerance + max iterations input fields to all pages
- [x] Show a result panel: root value, iterations, converged: yes/no
- [x] Add a status bar at the bottom of the window
- [x] Add NUM-CORE logo/branding to sidebar header

## Files to Edit

- `numcore_gui/dashboard.py`
- `numcore_gui/pages/root_finder_page.py`
- `numcore_gui/pages/network_solver_page.py`
- `numcore_gui/pages/calculus_page.py`
