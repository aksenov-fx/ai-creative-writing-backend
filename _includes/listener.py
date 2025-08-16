import os
import socketserver
from .process_request import process_request

class RequestHandler(socketserver.BaseRequestHandler):

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def process_tcp_data(self, data):
        args = data.split(',', 5)
        folder_path, file_path, method_name, chat_mode, part_value_str, selected_text = args 

        part_value = int(part_value_str)
        posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')
        posix_file_path = os.path.normpath(file_path).replace('\\', '/')
        chat_mode = chat_mode.lower() == 'true'

        return posix_folder_path, posix_file_path, method_name, chat_mode, part_value, selected_text

    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            data = self.request.recv(1024).decode('utf-8').strip()
            if not data: break
            
            folder, file, method, chat_mode,part_number, selected_text = self.process_tcp_data(data)

            if method not in ["story_remove_last_response", "chat_remove_last_response", "interrupt_write", "switch_debug"]:
                self.clear_screen()
                
            print("\nMethod: " + method + "\n")
            result = process_request(folder, file, method, chat_mode, part_number, selected_text)
            self.request.sendall(result.encode('utf-8'))
            
            break

# -------------------------------- #

def start_server():
    with socketserver.ThreadingTCPServer(('localhost', 9993), RequestHandler) as server:
        print("Server listening on port 9993")
        server.serve_forever()
        