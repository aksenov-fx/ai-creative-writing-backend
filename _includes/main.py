import os
import socketserver
import threading

from _includes import config, models
from .StoryGenerator.Utility import Utility
from .StoryGenerator.Chat import Chat

def process_request(data):

    folder_path, method_name, part_value, model_number = Utility.process_tcp_data(data)
    Utility.update_config(folder_path)

    os.system('clear' if os.name == 'posix' else 'cls')
    print("\nMethod: " + method_name + "\n")
    
    if method_name == "write_scene":
        Chat.write_scene(config.model)

    elif method_name == "custom_prompt":
        Chat.custom_prompt(config.model)

    elif method_name == "remove_last_response":
        Chat.remove_last_response()

    elif method_name == "remove_reasoning":
        Chat.remove_reasoning()

    elif method_name == "interrupt_write":
        config.interrupt_flag = True

    elif method_name == "rewrite":
        Chat.rewrite(config.model, part_value)

    elif method_name == "rewrite_parts":
        Chat.rewrite_parts(config.model, part_value)

    elif method_name == "regenerate":
        Chat.regenenerate(config.model, part_value)

    elif method_name == "add_part":
        Chat.add_part(config.model, part_value)

    elif method_name == "summarize":
        Chat.summarize(config.model)

    elif method_name == "update_summary":
        Chat.update_summary(config.model)

    elif method_name == "set_prompt":
        Chat.set_prompt(part_value)

    elif method_name == "set_model":
        config.model = list(models.values())[model_number -1]

    elif method_name == "enable_debug":
        config.debug = True

    elif method_name == "disable_debug":
        config.debug = False

    else:
        print(f"Unknown method: {method_name}")
        
# -------------------------------- #

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            # Expect format: "path:method_name:part_value:model_number"
            data = self.request.recv(1024).decode('utf-8').strip()
            if not data: break

            process_request(data)

# -------------------------------- #

# Create Listener and accept commands from TCP Server

def start_server():
    with socketserver.ThreadingTCPServer(('localhost', 9993), RequestHandler) as server:
        print("Server listening on port 9993")
        server.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()