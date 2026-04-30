## Goal
After any solver finishes, offer the user an option to export the full iteration
table to a CSV file. Uses Python's built-in `csv` module (no new dependencies).

## Expected Flow
```
Export results to CSV? (y/n) [n]: y
Enter filename [results.csv]:
Saved: results_newton_raphson.csv
```

## Tasks
- [ ] Add `export_steps_to_csv(steps, filename, method)` static method to `NumericalFormatter`
- [ ] CSV columns should match the method-specific table (x_n, f(x_n), etc.)
- [ ] Add the export prompt after every `run_*()` method call in `terminal.py`
- [ ] Show success / failure message with file path

## Files to Edit
- `numcore_cli/formatter.py`
- `numcore_cli/terminal.py`