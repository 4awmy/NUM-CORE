function result = ask_yes_no(prompt)
%ASK_YES_NO  Display a yes/no prompt; returns true for 'y', false for 'n'.

    while true
        s = strtrim(lower(input(sprintf('  >> %s [y/n]: ', prompt), 's')));
        if strcmp(s, 'y')
            result = true;
            return;
        elseif strcmp(s, 'n')
            result = false;
            return;
        end
        fprintf('  [!] Please enter y or n.\n');
    end
end
