import os
import socketserver
import threading

from _includes import config, endpoints
from .config import read_yaml, update_config_from_yaml
from .StoryGenerator.ChatHistory import ChatHistory
from .methods import Chat

def _update_config(folder_path):

    update_config_from_yaml(config, f'{folder_path}/Settings/settings.yaml')
    new_dict = read_yaml(f'{folder_path}/Settings/abbreviations.yaml')
    config.abbreviations.update(new_dict)
    config.first_prompt = open(f'{folder_path}/Settings/introduction.md', 'r').read()

    config.history_path = folder_path + '/' + config.history_path
    config.summary_path = folder_path + '/' + config.summary_path

    config.interrupt_flag = False

def process_request(folder_path, method_name, part_value, model_number=1):

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
        ChatHistory.set_prompt(folder_path, part_value)
        user_prompt = ChatHistory.expand_abbreviations(config.user_prompt)
        print(user_prompt)

    elif method_name == "set_model":
        model_number -= 1
        config.model = list(endpoints.models.values())[model_number]

    elif method_name == "enable_debug":
        config.debug = True

    elif method_name == "disable_debug":
        config.debug = False

    else:
        print(f"Unknown method: {method_name}")

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            data = self.request.recv(1024).decode('utf-8').strip()
            if not data: break

            # Expect format: "path:method_name:part_value:model_number"
            folder_path, method_name, part_value_str, model_number = data.split(',')
            part_value = int(part_value_str)
            model_number = int(model_number)
            posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')

            os.system('clear' if os.name == 'posix' else 'cls')
            print("\nMethod: " + method_name + "\n")

            _update_config(posix_folder_path)
            process_request(posix_folder_path, method_name, part_value, model_number)

# -------------------------------- #

# Create Listener and accept commands from TCP Server

def start_server():
    with socketserver.ThreadingTCPServer(('localhost', 9993), RequestHandler) as server:
        print("Server listening on port 9993")
        server.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()