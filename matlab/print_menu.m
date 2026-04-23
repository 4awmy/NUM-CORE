function print_menu(options)
%PRINT_MENU  Print a numbered list of options inside an ASCII border.
%
%   print_menu(options)   where options is a cell array of strings.

    fprintf('  +-- Select an Option ');
    fprintf('%s+\n', repmat('-', 1, 42));

    for i = 1:numel(options)
        fprintf('  |  [%d]  %-52s|\n', i, options{i});
    end

    fprintf('  +');
    fprintf('%s+\n\n', repmat('-', 1, 62));
end
