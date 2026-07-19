import threading
import code
import signal
import argparse
import sys
from .listener import start_server


def main():

    parser = argparse.ArgumentParser(
        description='Story Writer backend server.',
    )
    parser.add_argument(
        '--config', '-c',
        dest='settings_folder',
        default=None,
        help='Path to the config settings folder (default: ./_includes/settings/).',
    )
    parser.parse_args()

    # Handle Ctrl+C gracefully in code.interact mode and exit the application forcefully
    def handle_sigint(signum, frame):
        print('\nProgram terminated by user')
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handle_sigint)

    try:
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        code.interact(banner="", local=locals())
    
    except Exception as e:
        print(f'\nError: {e}')

if __name__ == "__main__":
    main()
