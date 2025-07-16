import os
import socketserver
import threading

from .methods import Chat
from .settings import config, update_config_from_yaml
from .abbreviations import update_abbreviations
from .StoryGenerator.ChatHistory import ChatHistory
from . import endpoints as endpoints

def process_request(folder_path, method_name, part_value, model_number=1):

    posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')

    update_config_from_yaml(config, f'{posix_folder_path}/Settings/settings.yaml')
    update_abbreviations(f'{posix_folder_path}/Settings/abbreviations.yaml')
    config.first_prompt = open(f'{posix_folder_path}/Settings/introduction.md', 'r').read()

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
        part_value -= 1
        ChatHistory.set_prompt(posix_folder_path, part_value)
        print(config.user_prompt)

    elif method_name == "set_model":
        model_number -= 1
        config.model = list(endpoints.models.values())[model_number]
        ChatHistory.set_prompt(posix_folder_path, part_value)

    elif method_name == "enable_debug":
        config.debug = True

    elif method_name == "disable_debug":
        config.debug = False

    else:
        print(f"Unknown method: {method_name}")

class PathHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            data = self.request.recv(1024).decode('utf-8').strip()
            if not data: break

            # Expect format: "path:method_name:part_value:model_number"
            folder_path, method_name, part_value_str, model_number = data.split(',')
            part_value = int(part_value_str)
            model_number = int(model_number)

            print("\nMethod: " + method_name + "\n")
            process_request(folder_path, method_name, part_value, model_number)

# -------------------------------- #

# Create Listener and accept commands from TCP Server

def start_server():
    with socketserver.ThreadingTCPServer(('localhost', 9993), PathHandler) as server:
        print("Server listening on port 9993")
        server.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)