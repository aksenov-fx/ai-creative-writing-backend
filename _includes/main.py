import threading
import code
import signal
from .listener import start_server
import sys


def main():

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