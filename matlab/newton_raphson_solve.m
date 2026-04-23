function [root, steps] = newton_raphson_solve(expr_str, x0, tol, max_iter)
%NEWTON_RAPHSON_SOLVE  Find root of f(x)=0 by Newton-Raphson iteration.
%
%   [root, steps] = newton_raphson_solve(expr_str, x0, tol, max_iter)
%
%   expr_str  - f(x) as a MATLAB expression string (e.g. 'x^3 - 2')
%   x0        - Initial guess
%   tol       - Convergence tolerance          (default 1e-6)
%   max_iter  - Maximum number of iterations  (default 100)
%
%   root      - Approximate root
%   steps     - Struct array with fields: iter, x, fx, dfx, error

    if nargin < 3 || isempty(tol),      tol      = 1e-6; end
    if nargin < 4 || isempty(max_iter), max_iter = 100;  end

    % ── Build callable f(x) ──────────────────────────────────────────────────
    f = str2func(['@(x) ' expr_str]);

    % ── Symbolic derivative (Symbolic Math Toolbox) ───────────────────────────
    use_symbolic = true;
    try
        syms x_sym
        f_sym  = str2sym(expr_str);
        df_sym = diff(f_sym, x_sym);
        df     = matlabFunction(df_sym, 'Vars', {x_sym});
    catch
        % Fallback: central-difference numerical derivative
        use_symbolic = false;
        h  = 1e-7;
        df = @(x) (f(x + h) - f(x - h)) / (2 * h);
    end

    if ~use_symbolic
        fprintf('  [i] Symbolic Toolbox unavailable – using numerical derivative.\n\n');
    end

    % ── Iteration ─────────────────────────────────────────────────────────────
    x_n   = x0;
    steps = struct('iter', {}, 'x', {}, 'fx', {}, 'dfx', {}, 'error', {});

    for i = 1:max_iter
        fx  = f(x_n);
        dfx = df(x_n);

        if abs(dfx) < 1e-12
            warning('NUM-CORE:zeroDeriv', ...
                'Derivative is near zero at x=%.6g. Stopping early.', x_n);
            break;
        end

        x_next = x_n - fx / dfx;
        err    = abs(x_next - x_n);

        steps(end+1).iter  = i;       %#ok<AGROW>
        steps(end).x       = x_next;
        steps(end).fx      = fx;
        steps(end).dfx     = dfx;
        steps(end).error   = err;

        x_n = x_next;

        if err < tol
            break;
        end
    end

    root = x_n;
end
