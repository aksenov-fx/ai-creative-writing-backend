import os
import socketserver
from .app.dispatcher import dispatch
from _includes import config
import traceback

class RequestHandler(socketserver.BaseRequestHandler):

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def process_tcp_data(self, data):
        if not data or not isinstance(data, str):
            raise ValueError("Invalid input data")
        
        args = data.split(',', 5)
        if len(args) != 6:
            raise ValueError(f"Expected 6 comma-separated values, got {len(args)}")
        
        folder_path, file_path, mode, method, part_value_str, selected_text = args
        
        # Validate and convert part number
        try:
            part_value = int(part_value_str)
        except ValueError:
            raise ValueError(f"Invalid part number: {part_value_str}")
        
        posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')
        posix_file_path = os.path.normpath(file_path).replace('\\', '/')

        return posix_folder_path, posix_file_path, mode, method, part_value, selected_text
    
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            try:
                data = self.request.recv(config.BUFFER_SIZE).decode('utf-8').strip()
                if not data: break
                
                folder, file, mode, method, part_number, selected_text = self.process_tcp_data(data)

                exempt_methods = ['story_remove_last_response', 'chat_remove_last_response', 'interrupt_write', 'switch_debug']
                if method not in exempt_methods: self.clear_screen()
                print(f"\nMethod: {method}\n")
                
                result = dispatch(folder, file, mode, method, part_number, selected_text)
                if result: self.request.sendall(result.encode('utf-8'))
                
            except ValueError as e:
                error_msg = f"Input validation error: {traceback.format_exc()}"
                print(error_msg)
                self.request.sendall(error_msg.encode('utf-8'))
            except Exception as e:
                error_msg = f"Processing error: {traceback.format_exc()}"
                print(error_msg)
                self.request.sendall(error_msg.encode('utf-8'))
            break

# -------------------------------- #

def start_server():
    with socketserver.ThreadingTCPServer(('localhost', config.PORT), RequestHandler) as server:
        print("Server listening on port " + str(config.PORT))
        server.serve_forever()
        