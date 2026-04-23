function run_simple_iteration()
%RUN_SIMPLE_ITERATION  Interactive UI for the Simple Iteration (Fixed-Point) solver.

    clc;
    print_header('Simple Iteration Method', 'Root Finding:  x_{n+1} = g(x_n)');

    fprintf('  Method Description:\n');
    fprintf('  Transform f(x)=0 into x=g(x) and iterate until convergence.\n');
    fprintf('  Convergence requires |g''(x)| < 1 near the root.\n\n');

    use_example = ask_yes_no('Load engineering example (x = cos(x))?');

    if use_example
        expr_str = 'cos(x)';
        x0       = 0.5;
        tol      = 1e-6;
        max_iter = 100;
        fprintf('\n  [EXAMPLE]  g(x) = %s\n', expr_str);
        fprintf('             x0   = %g\n', x0);
        fprintf('             tol  = %g,  max_iter = %d\n\n', tol, max_iter);
    else
        fprintf('\n  Enter g(x) using MATLAB syntax  (solve x = g(x)).\n');
        fprintf('  Examples:  cos(x)    |   (x^2 + 2) / 3\n\n');
        expr_str = input('  g(x) = ', 's');

        x0       = input('  Initial guess x0         : ');
        tol_raw  = input('  Tolerance      [1e-6]    : ');
        iter_raw = input('  Max iterations [100]     : ');

        if isempty(tol_raw),  tol      = 1e-6; else, tol      = tol_raw;  end
        if isempty(iter_raw), max_iter = 100;  else, max_iter = iter_raw; end
    end

    fprintf('\n  Running solver...\n\n');

    try
        [root, steps] = simple_iteration_solve(expr_str, x0, tol, max_iter);

        % ── Print iteration table ─────────────────────────────────────────────
        fprintf('  %-6s  %-22s  %-22s  %-12s\n', ...
                'Iter', 'x_n+1 = g(x_n)', 'x_n', 'Error');
        fprintf('  %s\n', repmat('-', 1, 68));
        for k = 1:length(steps)
            s = steps(k);
            fprintf('  %-6d  %-22.10f  %-22.10f  %-12.4e\n', ...
                    s.iter, s.x, s.gx, s.error);
        end
        fprintf('  %s\n', repmat('-', 1, 68));

        print_result(sprintf('Root = %.10f   |   Iterations: %d', root, length(steps)));

    catch ME
        fprintf('\n  [ERROR] %s\n', ME.message);
    end

    input('\n  Press Enter to return to menu...', 's');
end
