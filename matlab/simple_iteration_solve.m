function [root, steps] = simple_iteration_solve(expr_str, x0, tol, max_iter)
%SIMPLE_ITERATION_SOLVE  Find fixed point of x = g(x) by simple iteration.
%
%   [root, steps] = simple_iteration_solve(expr_str, x0, tol, max_iter)
%
%   expr_str  - g(x) as a MATLAB expression string (e.g. 'cos(x)')
%   x0        - Initial guess
%   tol       - Convergence tolerance          (default 1e-6)
%   max_iter  - Maximum number of iterations  (default 100)
%
%   root      - Approximate fixed point (root)
%   steps     - Struct array with fields: iter, x, gx, error

    if nargin < 3 || isempty(tol),      tol      = 1e-6; end
    if nargin < 4 || isempty(max_iter), max_iter = 100;  end

    % ── Build callable g(x) ──────────────────────────────────────────────────
    g = str2func(['@(x) ' expr_str]);

    % ── Iteration ─────────────────────────────────────────────────────────────
    x_n   = x0;
    steps = struct('iter', {}, 'x', {}, 'gx', {}, 'error', {});

    for i = 1:max_iter
        x_next = g(x_n);
        err    = abs(x_next - x_n);

        steps(end+1).iter  = i;       %#ok<AGROW>
        steps(end).x       = x_next;
        steps(end).gx      = x_next;
        steps(end).error   = err;

        x_n = x_next;

        if err < tol
            break;
        end

        if ~isfinite(x_n)
            error('NUM-CORE:diverge', ...
                'Sequence diverged at iteration %d. g(x) may not converge.', i);
        end
    end

    root = x_n;
end
