import sys
from numcore_cli.terminal import launch_cli

def main():
    """
    Main entry point for the NUM-CORE application.
    Launches the CLI terminal or the future GUI dashboard.
    """
    # In the future, we can add logic to choose between CLI and GUI
    # For now, we launch the robust rich-based CLI.
    try:
        launch_cli()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"[CRITICAL ERROR] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
