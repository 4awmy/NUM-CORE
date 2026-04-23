function [result, step] = numerical_integration(x_pts, y_pts, method)
%NUMERICAL_INTEGRATION  Numerical integration by Trapezoidal or Simpson rules.
%
%   [result, step] = numerical_integration(x_pts, y_pts, method)
%
%   x_pts  - Uniformly spaced x data points (vector)
%   y_pts  - Corresponding y = f(x) values  (vector)
%   method - 'trapezoidal' | 'simpson13' | 'simpson38'
%
%   result - Scalar integral estimate
%   step   - Struct with fields: method, h, n, formula, result

    x_pts = x_pts(:)';
    y_pts = y_pts(:)';
    n     = length(x_pts) - 1;   % number of intervals

    if nargin < 3 || isempty(method)
        method = 'trapezoidal';
    end
    method = lower(method);

    if length(y_pts) ~= length(x_pts) || n < 1
        error('NUM-CORE:badInput', 'x_pts and y_pts must be the same length >= 2.');
    end

    % ── Verify uniform spacing ─────────────────────────────────────────────────
    h_vec = diff(x_pts);
    if ~all(abs(h_vec - h_vec(1)) < 1e-10 * abs(h_vec(1)))
        error('NUM-CORE:nonUniform', 'x_pts must be uniformly spaced.');
    end
    h = h_vec(1);

    % ── Compute integral ───────────────────────────────────────────────────────
    switch method
        case 'trapezoidal'
            result  = (h/2) * (y_pts(1) + 2*sum(y_pts(2:end-1)) + y_pts(end));
            formula = 'h/2 * [ f0 + 2*(f1+...+fn-1) + fn ]';

        case 'simpson13'
            if mod(n, 2) ~= 0
                error('NUM-CORE:badIntervals', ...
                    'Simpson''s 1/3 rule requires an even number of intervals (got %d).', n);
            end
            result  = (h/3) * (y_pts(1) ...
                        + 4*sum(y_pts(2:2:end-1)) ...
                        + 2*sum(y_pts(3:2:end-2)) ...
                        + y_pts(end));
            formula = 'h/3 * [ f0 + 4*(odd) + 2*(even) + fn ]';

        case 'simpson38'
            if mod(n, 3) ~= 0
                error('NUM-CORE:badIntervals', ...
                    'Simpson''s 3/8 rule requires intervals divisible by 3 (got %d).', n);
            end
            s = y_pts(1) + y_pts(end);
            for i = 2:n
                if mod(i-1, 3) == 0
                    s = s + 2 * y_pts(i);
                else
                    s = s + 3 * y_pts(i);
                end
            end
            result  = (3*h/8) * s;
            formula = '3h/8 * [ f0 + 3*(non-mult3) + 2*(mult3) + fn ]';

        otherwise
            error('NUM-CORE:unknownMethod', ...
                'Unknown method "%s". Use trapezoidal, simpson13, or simpson38.', method);
    end

    % ── Build output struct ────────────────────────────────────────────────────
    step.method  = method;
    step.h       = h;
    step.n       = n;
    step.formula = formula;
    step.result  = result;
end
