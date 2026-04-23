function print_header(title, subtitle)
%PRINT_HEADER  Display a formatted ASCII header box.
%
%   print_header(title)
%   print_header(title, subtitle)

    WIDTH = 62;
    BORDER = repmat('=', 1, WIDTH);

    fprintf('\n');
    fprintf('  +%s+\n', BORDER);
    fprintf('  |%s|\n', pad_center(title, WIDTH));
    if nargin > 1 && ~isempty(subtitle)
        fprintf('  |%s|\n', pad_center(subtitle, WIDTH));
    end
    fprintf('  |%s|\n', repmat(' ', 1, WIDTH));
    fprintf('  +%s+\n\n', BORDER);
end

% ── local helpers ─────────────────────────────────────────────────────────────

function s = pad_center(txt, width)
    n       = length(txt);
    padding = max(0, width - n);
    lpad    = floor(padding / 2);
    rpad    = padding - lpad;
    s       = [repmat(' ', 1, lpad), txt, repmat(' ', 1, rpad)];
end
