import sys
import argparse
import os
import matplotlib.pyplot as plt
from rich.console import Console

from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.align import Align
from rich.text import Text
from rich.table import Table

from numcore_cli.terminal import launch_cli
from numcore_gui import launch_gui

def display_startup_menu():
    """
    Displays a visual startup menu to choose between TUI and GUI.
    """
    console = Console()
    console.clear()
    
    header_text = Text()
    header_text.append(" NUM-CORE ", style="bold white on cyan")
    header_text.append("\nNumerical Methods Suite", style="italic dim")
    
    console.print(Align.center(Panel(
        header_text,
        border_style="cyan",
        padding=(1, 2),
        expand=False
    )))
    console.print()

    options = [
        "Terminal User Interface (TUI)",
        "Graphical User Interface (GUI)",
        "Exit"
    ]
    
    menu_table = Table.grid(padding=(0, 1))
    for i, option in enumerate(options, 1):
        menu_table.add_row(
            Text(f"{i}.", style="bold magenta"),
            Text(option, style="white")
        )
    
    console.print(Align.center(Panel(
        menu_table,
        title="[bold]Select Startup Mode[/bold]",
        title_align="left",
        border_style="dim",
        padding=(1, 2),
        expand=False
    )))
    
    choice = IntPrompt.ask(
        "Enter your choice",
        choices=[str(i) for i in range(1, len(options) + 1)],
        show_choices=False
    )
    
    return choice

def main():
    """
    Main entry point for the NUM-CORE application.
    Parses arguments and launches the chosen interface.
    """
    console = Console()
    # Register custom Matplotlib style for True Black theme
    style_path = os.path.join(os.path.dirname(__file__), "numcore_gui", "styles", "numcore_black.mplstyle")
    if os.path.exists(style_path):
        plt.style.use(style_path)

    parser = argparse.ArgumentParser(
        description="NUM-CORE: A Professional Numerical Computation Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --tui    # Launch Terminal Interface
  python main.py --gui    # Launch Graphical Interface
        """
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tui", action="store_true", help="Start the Terminal User Interface")
    group.add_argument("--gui", action="store_true", help="Start the Graphical User Interface")
    
    args = parser.parse_args()

    try:
        if args.tui:
            launch_cli()
        elif args.gui:
            launch_gui()
        else:
            # No flags provided, show interactive menu
            choice = display_startup_menu()
            if choice == 1:
                launch_cli()
            elif choice == 2:
                launch_gui()
            else:
                console.print("[bold yellow][SYSTEM][/bold yellow] Exiting...")
                sys.exit(0)
                
    except KeyboardInterrupt:
        console.print("\n[bold yellow][SYSTEM][/bold yellow] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        import traceback
        console.print(f"\n[bold red][CRITICAL ERROR][/bold red] {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()