function run_integration()
%RUN_INTEGRATION  Interactive UI for numerical integration solver.

    clc;
    print_header('Numerical Integration', 'Trapezoidal / Simpson''s 1/3 / Simpson''s 3/8');

    fprintf('  Method Description:\n');
    fprintf('  Approximate the definite integral of data given at discrete points.\n');
    fprintf('  Trapezoidal: any n intervals.  Simpson 1/3: even n.  Simpson 3/8: n mod 3 = 0.\n\n');

    use_example = ask_yes_no('Load engineering example (rocket velocity)?');

    if use_example
        x_pts  = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0];
        y_pts  = [0.0, 227.0, 362.0, 517.0, 602.0, 756.0, 901.0];
        method = 'simpson13';
        fprintf('\n  [EXAMPLE]  Rocket velocity vs. time  (distance = integral of v dt)\n');
        fprintf('  t  (s)   : %s\n', mat2str(x_pts));
        fprintf('  v  (m/s) : %s\n', mat2str(y_pts));
        fprintf('  Method   : %s\n\n', method);
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

        fprintf('\n  Available methods:\n');
        fprintf('    [1] trapezoidal\n');
        fprintf('    [2] simpson13\n');
        fprintf('    [3] simpson38\n\n');
        method_choice = get_int_choice(1, 3);

        methods = {'trapezoidal', 'simpson13', 'simpson38'};
        method  = methods{method_choice};
    end

    fprintf('\n  Running solver...\n\n');

    try
        [result, step] = numerical_integration(x_pts, y_pts, method);

        % ── Print integration summary ─────────────────────────────────────────
        fprintf('  Integration Summary:\n');
        fprintf('  %s\n', repmat('-', 1, 50));
        fprintf('  Method   : %s\n', step.method);
        fprintf('  Formula  : %s\n', step.formula);
        fprintf('  h (step) : %.6f\n', step.h);
        fprintf('  n (intvl): %d\n',   step.n);
        fprintf('  %s\n', repmat('-', 1, 50));

        print_result(sprintf('Integral = %.10f', result));

    catch ME
        fprintf('\n  [ERROR] %s\n', ME.message);
    end

    input('\n  Press Enter to return to menu...', 's');
end
