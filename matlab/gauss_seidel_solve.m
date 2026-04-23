function [x, steps, converged] = gauss_seidel_solve(A, b, x0, tol, max_iter)
%GAUSS_SEIDEL_SOLVE  Solve Ax=b iteratively using the Gauss-Seidel method.
%
%   [x, steps, converged] = gauss_seidel_solve(A, b, x0, tol, max_iter)
%
%   A        - n×n coefficient matrix
%   b        - n×1 right-hand side vector
%   x0       - Initial guess (default: zeros)
%   tol      - Convergence tolerance          (default 1e-6)
%   max_iter - Maximum number of iterations  (default 100)
%
%   x         - Solution vector
%   steps     - Struct array with fields: iter, x, error
%   converged - true if tolerance was met

    n = size(A, 1);

    if nargin < 3 || isempty(x0),      x0       = zeros(n,1); end
    if nargin < 4 || isempty(tol),     tol      = 1e-6;       end
    if nargin < 5 || isempty(max_iter),max_iter = 100;        end

    % ── Enforce diagonal dominance via row swapping ───────────────────────────
    [A, b] = enforce_diagonal_dominance(A, b);

    % ── Check for zero diagonal ───────────────────────────────────────────────
    for i = 1:n
        if abs(A(i,i)) < 1e-12
            error('NUM-CORE:zeroDiag', ...
                'Zero diagonal at row %d after pivoting. Matrix may be singular.', i);
        end
    end

    % ── Iteration ─────────────────────────────────────────────────────────────
    x         = x0(:);
    steps     = struct('iter', {}, 'x', {}, 'error', {});
    converged = false;

    for k = 1:max_iter
        x_old = x;

        for i = 1:n
            sigma = A(i,:) * x - A(i,i) * x(i);   % uses latest x values
            x(i)  = (b(i) - sigma) / A(i,i);
        end

        err = norm(x - x_old, inf);

        steps(end+1).iter  = k;        %#ok<AGROW>
        steps(end).x       = x';
        steps(end).error   = err;

        if err < tol
            converged = true;
            break;
        end
    end
end

% ── Local: row-swap to maximise diagonal entries ───────────────────────────────

function [A_out, b_out] = enforce_diagonal_dominance(A, b)
    n     = size(A,1);
    A_out = A;
    b_out = b(:);

    for i = 1:n
        [~, max_row] = max(abs(A_out(i:end, i)));
        max_row = max_row + i - 1;

        if max_row ~= i
            A_out([i, max_row], :)  = A_out([max_row, i], :);
            b_out([i, max_row])     = b_out([max_row, i]);
        end
    end
end
