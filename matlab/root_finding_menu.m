function root_finding_menu()
%ROOT_FINDING_MENU  Root finding sub-menu loop.

    while true
        clc;
        print_header('Root Finding', 'Solve for f(x) = 0');

        options = {
            'Newton-Raphson Method   (uses derivative for fast convergence)', ...
            'Simple Iteration Method (fixed-point  x = g(x))', ...
            'Back to Main Menu'
        };
        print_menu(options);

        choice = get_int_choice(1, numel(options));

        switch choice
            case 1,  run_newton_raphson();
            case 2,  run_simple_iteration();
            case 3,  break;
        end
    end
end
