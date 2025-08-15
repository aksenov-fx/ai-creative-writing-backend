import socketserver
import threading

from _includes import config
from .app.Utility import Utility
from .app.Composers.PromptComposer import set_prompt
from .app.Chat import Chat
from .app.History.Factory import Factory
from .app.ConfigManager import get_story_config, override_config, get_chat_config

def process_request(folder: str, file: str, method: str, chat_mode: bool, part_number: str, selected_text: str):

    result = ""

    if chat_mode: new_config = get_chat_config(file)
    else:         new_config = get_story_config(folder)

    with override_config(config, **new_config):
        
        if method == "write_scene":         
            Chat.write_scene()
        elif method == "custom_prompt":     
            Chat.custom_prompt()
        elif method == "rewrite_selection": 
            result = Chat.rewrite_selection(selected_text)
        elif method == "translate":         
            result = Chat.translate(selected_text)
        elif method == "explain":           
            result = Chat.explain(selected_text)
        elif method == "rewrite_part":      
            Chat.change_part(part_number)
        elif method == "rewrite_parts":     
            Chat.change_parts(part_number)
        elif method == "regenerate":        
            Chat.regenerate(part_number)
        elif method == "add_part":          
            Chat.add_part(part_number)
        elif method == "update_summary":    
            Chat.update_summary()
        elif method == "chat":              
            Chat.chat(file)
        elif method == "story_remove_last_response":
            Factory.get_story().remove_last_response()
        elif method == "chat_remove_last_response":
            Factory.get_chat_history(file).remove_last_response()
    
    # No config override
    if method == "interrupt_write":      
        config.interrupt_flag = True

    elif method == "switch_debug":       
        config.debug = not config.debug
        print("Debug mode is on") if config.debug else print("Debug mode is off")
    
    elif method == "set_prompt":
        set_prompt(part_number, new_config['abbreviations'])

    return result

# -------------------------------- #

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self): #method is called automatically by server upon receiving a new request

        while True:
            data = self.request.recv(1024).decode('utf-8').strip()
            if not data: break
            
            folder, file, method, chat_mode,part_number, selected_text = Utility.process_tcp_data(data)

            if method not in ["story_remove_last_response", "chat_remove_last_response", "interrupt_write", "switch_debug"]:
                Utility.clear_screen()
                
            print("\nMethod: " + method + "\n")
            result = process_request(folder, file, method, chat_mode, part_number, selected_text)
            self.request.sendall(result.encode('utf-8'))
            
            break

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