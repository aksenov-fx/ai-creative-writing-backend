import threading
import code
from .listener import start_server

def main():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    code.interact(banner="", local=locals())

if __name__ == "__main__":
    main()