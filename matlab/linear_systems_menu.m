function linear_systems_menu()
%LINEAR_SYSTEMS_MENU  Linear systems sub-menu loop.

    while true
        clc;
        print_header('Linear Systems', 'Solve  Ax = b');

        options = {
            'Gauss-Seidel Method  (iterative solver with auto diagonal dominance)', ...
            'Back to Main Menu'
        };
        print_menu(options);

        choice = get_int_choice(1, numel(options));

        switch choice
            case 1,  run_gauss_seidel();
            case 2,  break;
        end
    end
end
