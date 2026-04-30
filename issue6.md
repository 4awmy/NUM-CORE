## Goal
When running `python main.py`, show a startup menu so the user can pick between
the TUI and the GUI. Also support `--tui` / `--gui` flags to skip the menu.

## Expected Output
```
+==================================+
|         NUM-CORE v2.0            |
+==================================+
|  1.  Terminal Interface (TUI)    |
|  2.  Graphical Dashboard (GUI)   |
|  3.  Exit                        |
+==================================+
```

## Tasks
- [ ] Use Rich Panel + IntPrompt for the selector menu
- [ ] Choice 1 → `launch_cli()`
- [ ] Choice 2 → `from numcore_gui.dashboard import Dashboard; Dashboard().mainloop()`
- [ ] Choice 3 → `sys.exit(0)`
- [ ] Add argparse: `python main.py --tui` or `python main.py --gui` skips the menu

## Files to Edit
- `main.py`