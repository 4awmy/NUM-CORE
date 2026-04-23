function [coef, result_y, steps] = ndd_interpolation(x_pts, y_pts, target_x)
%NDD_INTERPOLATION  Newton's Divided Difference interpolation.
%
%   [coef, result_y, steps] = ndd_interpolation(x_pts, y_pts)
%   [coef, result_y, steps] = ndd_interpolation(x_pts, y_pts, target_x)
%
%   x_pts    - Vector of x data points
%   y_pts    - Vector of y data points
%   target_x - (Optional) x value(s) to interpolate
%
%   coef     - Divided difference coefficients
%   result_y - Interpolated y value(s) at target_x (or y_pts if none given)
%   steps    - Struct array with fields: order, coef

    x_pts = x_pts(:)';   % row vectors
    y_pts = y_pts(:)';
    n     = length(x_pts);

    if length(y_pts) ~= n || n < 2
        error('NUM-CORE:badInput', 'x_pts and y_pts must have the same length >= 2.');
    end

    % ── Build divided difference table ────────────────────────────────────────
    dd = zeros(n, n);
    dd(:,1) = y_pts(:);

    steps = struct('order', {}, 'coef', {});
    steps(1).order = 0;
    steps(1).coef  = dd(1,1);

    for j = 2:n
        for i = j:n
            dd(i,j) = (dd(i,j-1) - dd(i-1,j-1)) / (x_pts(i) - x_pts(i-j+1));
        end
        steps(j).order = j - 1;
        steps(j).coef  = dd(j,j);
    end

    coef = diag(dd);   % leading diagonal = Newton coefficients

    % ── Evaluate Newton polynomial ─────────────────────────────────────────────
    if nargin >= 3 && ~isempty(target_x)
        result_y = arrayfun(@(xv) newton_poly_eval(coef, x_pts, xv), target_x);
    else
        result_y = y_pts;
    end
end

% ── Local: Horner-style Newton polynomial evaluation ──────────────────────────

function y = newton_poly_eval(coef, x_pts, xv)
    n = length(coef);
    y = coef(1);
    for i = 2:n
        term = coef(i);
        for j = 1:i-1
            term = term * (xv - x_pts(j));
        end
        y = y + term;
    end
end
