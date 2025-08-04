import socketserver
import threading

from _includes import config
from .app.Utility import Utility
from .app.Chat import Chat
from .app.Factory import Factory
from .app.ConfigManager import update_config, override_config

def process_request(folder: str, method: str, part_number: str):

    new_config = update_config(folder)
    with override_config(config, **new_config):
        
        if method == "write_scene":      Chat.write_scene()
        elif method == "custom_prompt":  Chat.custom_prompt()
        elif method == "rewrite":        Chat.change_part(part_number)
        elif method == "rewrite_parts":  Chat.change_parts(part_number)
        elif method == "regenerate":     Chat.regenerate(part_number)
        elif method == "add_part":       Chat.add_part(part_number)
        elif method == "summarize":      Chat.summarize_all()
        elif method == "update_summary": Chat.update_summary()
        elif method == "remove_last_response":
            Factory.get_story().remove_last_response()
    
    # No config override
    if method == "interrupt_write":      config.interrupt_flag = True
    elif method == "enable_debug":       config.debug = True
    elif method == "disable_debug":      config.debug = False
    elif method == "set_prompt":
        Utility.set_prompt(part_number, new_config['abbreviations'])

# -------------------------------- #

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            # Expect format: "path,method,part_value"
            data = self.request.recv(1024).decode('utf-8').strip()
            if not data: break
            
            folder, method, part_number = Utility.process_tcp_data(data)
            Utility.clear_screen()
            print("\nMethod: " + method + "\n")

            process_request(folder, method, part_number)

# -------------------------------- #

# Create Listener and accept commands from TCP Server

def start_server():
    with socketserver.ThreadingTCPServer(('localhost', 9993), RequestHandler) as server:
        print("Server listening on port 9993")
        server.serve_forever()
        
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

if __name__ == "__main__":
    import code
    code.interact(banner="", local=locals())