function run_interpolation()
%RUN_INTERPOLATION  Interactive UI for Newton's Divided Difference interpolation.

    clc;
    print_header('Interpolation', 'Newton''s Divided Difference');

    fprintf('  Method Description:\n');
    fprintf('  Builds a polynomial through known data points using divided differences.\n');
    fprintf('  Useful for estimating values between experimental data.\n\n');

    use_example = ask_yes_no('Load engineering example (specific heat of water)?');

    if use_example
        x_pts    = [0.0, 10.0, 20.0, 30.0, 40.0];
        y_pts    = [4.217, 4.192, 4.181, 4.178, 4.178];
        target_x = [25.0];
        fprintf('\n  [EXAMPLE]  Specific heat of water vs. Temperature\n');
        fprintf('  T  (C) : %s\n', mat2str(x_pts));
        fprintf('  Cp     : %s\n', mat2str(y_pts));
        fprintf('  Target : T = 25 C\n\n');
    else
        fprintf('\n  Enter data points (space-separated values):\n');

        while true
            x_str = input('  x points: ', 's');
            x_pts = str2num(x_str); %#ok<ST2NM>
            if ~isempty(x_pts) && length(x_pts) >= 2, break; end
            fprintf('  [!] Enter at least 2 x values.\n');
        end

        while true
            y_str = input('  y points: ', 's');
            y_pts = str2num(y_str); %#ok<ST2NM>
            if length(y_pts) == length(x_pts), break; end
            fprintf('  [!] Must have the same number of y values (%d).\n', length(x_pts));
        end

        tx_str   = input('  Target x value(s) to interpolate [Enter to skip]: ', 's');
        if isempty(strtrim(tx_str))
            target_x = [];
        else
            target_x = str2num(tx_str); %#ok<ST2NM>
        end
    end

    fprintf('\n  Running solver...\n\n');

    try
        [coef, result_y, steps] = ndd_interpolation(x_pts, y_pts, target_x);

        % ── Print divided difference coefficients ─────────────────────────────
        fprintf('  Divided Difference Coefficients:\n');
        fprintf('  %-8s  %-20s\n', 'Order', 'Coefficient');
        fprintf('  %s\n', repmat('-', 1, 32));
        for k = 1:length(steps)
            fprintf('  %-8d  %-20.10f\n', steps(k).order, steps(k).coef);
        end
        fprintf('  %s\n', repmat('-', 1, 32));

        % ── Print interpolated values ─────────────────────────────────────────
        if ~isempty(target_x)
            fprintf('\n  Interpolated Results:\n');
            fprintf('  %-14s  %-20s\n', 'x', 'Interpolated f(x)');
            fprintf('  %s\n', repmat('-', 1, 36));
            for k = 1:length(target_x)
                fprintf('  %-14.6f  %-20.10f\n', target_x(k), result_y(k));
            end
            fprintf('  %s\n', repmat('-', 1, 36));

            if length(result_y) == 1
                print_result(sprintf('f(%.4g) = %.10f', target_x(1), result_y(1)));
            else
                print_result(sprintf('%d values interpolated successfully.', length(result_y)));
            end
        else
            print_result(sprintf('Polynomial built with %d coefficients.', length(coef)));
        end

    catch ME
        fprintf('\n  [ERROR] %s\n', ME.message);
    end

    input('\n  Press Enter to return to menu...', 's');
end
