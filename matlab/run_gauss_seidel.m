function run_gauss_seidel()
%RUN_GAUSS_SEIDEL  Interactive UI for the Gauss-Seidel linear system solver.

    clc;
    print_header('Gauss-Seidel Method', 'Linear Systems:  Ax = b');

    fprintf('  Method Description:\n');
    fprintf('  Iterative solver for Ax=b. Efficient for large sparse matrices.\n');
    fprintf('  Applies automatic row-swapping to improve diagonal dominance.\n\n');

    use_example = ask_yes_no('Load engineering example (3x3 truss system)?');

    if use_example
        A        = [4, -1, -1; -1, 4, -1; -1, -1, 4];
        b        = [3; 2; 1];
        x0       = zeros(3,1);
        tol      = 1e-6;
        max_iter = 100;
        fprintf('\n  [EXAMPLE]  3x3 Truss Analysis\n');
        fprintf('  A =\n');  disp(A);
        fprintf('  b = [%s]\n\n', num2str(b'));
    else
        n = input('  Number of equations (n): ');
        if isempty(n) || n < 1
            fprintf('  [!] Invalid size.\n');
            input('  Press Enter to return...', 's');
            return;
        end

        A = zeros(n, n);
        fprintf('\n  Enter each row of A (space-separated):\n');
        for i = 1:n
            while true
                row_str = input(sprintf('  Row %d: ', i), 's');
                row     = str2num(row_str); %#ok<ST2NM>
                if length(row) == n
                    A(i,:) = row;
                    break;
                end
                fprintf('  [!] Expected %d values, got %d.\n', n, length(row));
            end
        end

        while true
            b_str = input('\n  Enter b vector (space-separated): ', 's');
            b     = str2num(b_str)'; %#ok<ST2NM>
            if length(b) == n, break; end
            fprintf('  [!] Expected %d values.\n', n);
        end

        x0_str   = input(sprintf('  Initial guess x0 [default zeros]: '), 's');
        x0_vals  = str2num(x0_str); %#ok<ST2NM>
        if length(x0_vals) == n
            x0 = x0_vals(:);
        else
            x0 = zeros(n,1);
        end

        tol_raw  = input('  Tolerance      [1e-6]: ');
        iter_raw = input('  Max iterations [100]  : ');

        if isempty(tol_raw),  tol      = 1e-6; else, tol      = tol_raw;  end
        if isempty(iter_raw), max_iter = 100;  else, max_iter = iter_raw; end
    end

    fprintf('\n  Running solver...\n\n');

    try
        [x, steps, converged] = gauss_seidel_solve(A, b, x0, tol, max_iter);

        % ── Print iteration table ─────────────────────────────────────────────
        n = length(x);
        hdr_vars = arrayfun(@(i) sprintf('x%d', i), 1:n, 'UniformOutput', false);
        hdr      = ['  Iter  ' sprintf('%-14s', hdr_vars{:}) '  Max-Error'];
        fprintf('%s\n', hdr);
        fprintf('  %s\n', repmat('-', 1, length(hdr)));
        for k = 1:length(steps)
            s      = steps(k);
            x_vals = sprintf('%-14.8f', s.x);
            fprintf('  %-6d  %s  %-12.4e\n', s.iter, x_vals, s.error);
        end
        fprintf('  %s\n', repmat('-', 1, length(hdr)));

        sol_str = ['[' sprintf(' %.8f', x) ' ]'];
        status  = ternary(converged, 'Converged', 'Max iterations reached');
        print_result(sprintf('x = %s   |   %s   |   %d iters', ...
                             sol_str, status, length(steps)));

    catch ME
        fprintf('\n  [ERROR] %s\n', ME.message);
    end

    input('\n  Press Enter to return to menu...', 's');
end

% ── Local helper ───────────────────────────────────────────────────────────────

function s = ternary(cond, a, b)
    if cond, s = a; else, s = b; end
end
