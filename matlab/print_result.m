function print_result(message)
%PRINT_RESULT  Print a highlighted result banner.
%
%   print_result(message)

    width  = max(60, length(message) + 6);
    border = repmat('*', 1, width);

    fprintf('\n');
    fprintf('  %s\n', border);
    fprintf('  *  %-*s*\n', width - 4, ['RESULT: ' message]);
    fprintf('  %s\n\n', border);
end
