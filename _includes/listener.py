import os
import socketserver
import threading

from .methods import Chat
from .settings import config, update_config_from_json
from .StoryGenerator.ChatHistory import ChatHistory
from . import endpoints as endpoints

def process_file(folder_path, method_name, part_value):

    posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')

    update_config_from_json(config, f'{posix_folder_path}/config.json')
    config.history_path = posix_folder_path + '/' + config.history_path
    config.interrupt_flag = False

    if method_name == "write_scene":
        Chat.write_scene(config.model)

    elif method_name == "custom_prompt":
        Chat.custom_prompt(config.model)

    elif method_name == "remove_last_response":
        ChatHistory.remove_last_response()

    elif method_name == "remove_reasoning":
        ChatHistory.remove_reasoning()

    elif method_name == "interrupt_write":
        config.interrupt_flag = True

    elif method_name == "refine":
        Chat.refine(config.model, part_value)

    elif method_name == "rewrite":
        Chat.rewrite(config.model, part_value)

    elif method_name == "regenerate":
        Chat.regenenerate(config.model, part_value)

    elif method_name == "add_part":
        Chat.add_part(config.model, part_value)

    elif method_name == "summarize":
        Chat.summarize(config.model)

    elif method_name == "update_summary":
        Chat.update_summary(config.model)

    elif method_name == "set_prompt":
        ChatHistory.set_prompt(posix_folder_path, part_value)

    else:
        print(f"Unknown method: {method_name}")

class PathHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            data = self.request.recv(1024).decode('utf-8').strip()
            if not data: break

            # Expect format: "path:method_name:part_value"
            folder_path, method_name, part_value_str = data.split(',')
            part_value = int(part_value_str)

            process_file(folder_path, method_name, part_value)

# -------------------------------- #

# Create Listener and accept commands from TCP Server

if not config.create_listener:
    exit()

def start_server():
    with socketserver.ThreadingTCPServer(('localhost', 9993), PathHandler) as server:
        print("Server listening on port 9993")
        server.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()