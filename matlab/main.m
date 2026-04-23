% ============================================================
%  NUM-CORE  —  Professional Numerical Computation Suite
%  MATLAB Edition
%
%  Usage:  Open MATLAB, cd to the 'matlab/' folder, then run:
%              >> main
%
%  Requirements:
%    - MATLAB R2019b or newer
%    - Symbolic Math Toolbox (for Newton-Raphson exact derivative)
%      A numerical-derivative fallback is used if unavailable.
% ============================================================

clc; clear; close all;

fprintf('\n');
fprintf('  ============================================================\n');
fprintf('  |           NUM-CORE  —  MATLAB Edition                    |\n');
fprintf('  |      Professional Numerical Computation Suite            |\n');
fprintf('  ============================================================\n');
fprintf('\n  Initialising...\n\n');
pause(0.5);

% ── Main menu loop ─────────────────────────────────────────────────────────────

while true
    clc;
    print_header('NUM-CORE', 'Professional Numerical Computation Suite');

    options = {
        'Root Finding   (Newton-Raphson, Simple Iteration)', ...
        'Linear Systems (Gauss-Seidel)', ...
        'Calculus       (Interpolation, Integration)', ...
        'Exit'
    };
    print_menu(options);

    choice = get_int_choice(1, numel(options));

    switch choice
        case 1
            root_finding_menu();
        case 2
            linear_systems_menu();
        case 3
            calculus_menu();
        case 4
            clc;
            fprintf('\n');
            fprintf('  +------------------------------------------------------------+\n');
            fprintf('  |          Exiting NUM-CORE.  Goodbye!                       |\n');
            fprintf('  |          Author: Omar Hossam  |  Numerical Methods         |\n');
            fprintf('  +------------------------------------------------------------+\n\n');
            break;
    end
end
