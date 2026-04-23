function choice = get_int_choice(min_val, max_val)
%GET_INT_CHOICE  Prompt user for an integer in [min_val, max_val].
%   Loops until valid input is received.

    while true
        raw = input(sprintf('  >> Choice [%d-%d]: ', min_val, max_val));
        if isnumeric(raw) && isscalar(raw) && ...
                floor(raw) == raw && raw >= min_val && raw <= max_val
            choice = raw;
            return;
        end
        fprintf('  [!] Please enter a whole number between %d and %d.\n\n', ...
                min_val, max_val);
    end
end
