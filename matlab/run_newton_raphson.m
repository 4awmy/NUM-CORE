function run_newton_raphson()
%RUN_NEWTON_RAPHSON  Interactive UI for the Newton-Raphson solver.

    clc;
    print_header('Newton-Raphson Method', 'Root Finding:  x_{n+1} = x_n - f(x_n)/f''(x_n)');

    fprintf('  Method Description:\n');
    fprintf('  Newton-Raphson uses the derivative of f(x) for rapid convergence.\n');
    fprintf('  Best suited for smooth, differentiable functions.\n\n');

    use_example = ask_yes_no('Load engineering example (floating ball depth)?');

    if use_example
        expr_str = 'x^3 - 0.165*x^2 + 3.993e-4';
        x0       = 0.05;
        tol      = 1e-6;
        max_iter = 100;
        fprintf('\n  [EXAMPLE]  f(x) = %s\n', expr_str);
        fprintf('             x0   = %g\n', x0);
        fprintf('             tol  = %g,  max_iter = %d\n\n', tol, max_iter);
    else
        fprintf('\n  Enter f(x) using MATLAB syntax.\n');
        fprintf('  Examples:  x^3 - 2*x - 5    |   sin(x) - x/2\n\n');
        expr_str = input('  f(x) = ', 's');

        x0       = input('  Initial guess x0         : ');
        tol_raw  = input('  Tolerance      [1e-6]    : ');
        iter_raw = input('  Max iterations [100]     : ');

        if isempty(tol_raw),  tol      = 1e-6; else, tol      = tol_raw;  end
        if isempty(iter_raw), max_iter = 100;  else, max_iter = iter_raw; end
    end

    fprintf('\n  Running solver...\n\n');

    try
        [root, steps] = newton_raphson_solve(expr_str, x0, tol, max_iter);

        % ── Print iteration table ─────────────────────────────────────────────
        fprintf('  %-6s  %-18s  %-18s  %-18s  %-12s\n', ...
                'Iter', 'x_n+1', 'f(x_n)', 'f''(x_n)', 'Error');
        fprintf('  %s\n', repmat('-', 1, 78));
        for k = 1:length(steps)
            s = steps(k);
            fprintf('  %-6d  %-18.10f  %-18.10f  %-18.10f  %-12.4e\n', ...
                    s.iter, s.x, s.fx, s.dfx, s.error);
        end
        fprintf('  %s\n', repmat('-', 1, 78));

        print_result(sprintf('Root = %.10f   |   Iterations: %d', root, length(steps)));

    catch ME
        fprintf('\n  [ERROR] %s\n', ME.message);
    end

    input('\n  Press Enter to return to menu...', 's');
end
