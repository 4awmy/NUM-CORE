function calculus_menu()
%CALCULUS_MENU  Calculus sub-menu loop.

    while true
        clc;
        print_header('Calculus', 'Interpolation & Numerical Integration');

        options = {
            'Interpolation  (Newton''s Divided Difference)', ...
            'Integration    (Trapezoidal / Simpson''s 1/3 / 3/8)', ...
            'Back to Main Menu'
        };
        print_menu(options);

        choice = get_int_choice(1, numel(options));

        switch choice
            case 1,  run_interpolation();
            case 2,  run_integration();
            case 3,  break;
        end
    end
end
