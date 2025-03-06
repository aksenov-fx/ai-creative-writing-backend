import tkinter as tk
import threading

from .chat_methods import Chat
from .chat_settings import config
from .StoryGenerator.ChatHistory import ChatHistory
from . import chat_endpoints as chat_endpoints

class ChatUI:
    def __init__(self):
        config.interrupt_flag = False
        self.ui_thread = None

    def create_window(self):
        def write_scene1():
            config.interrupt_flag = False
            write_thread = threading.Thread(target=Chat.write_scene, args=(chat_endpoints.models['deepseek'],))
            write_thread.start()

        def write_scene2():
            config.interrupt_flag = False
            write_thread = threading.Thread(target=Chat.write_scene, args=(chat_endpoints.models['qwen'],))
            write_thread.start()

        def custom_prompt():
            config.interrupt_flag = False
            write_thread = threading.Thread(target=Chat.custom_prompt, args=(chat_endpoints.models['deepseek'],))
            write_thread.start()
            
        def remove_last():
            ChatHistory.remove_last_response()
            
        def insert_response():
            ChatHistory.insert(config.assistant_response)
            
        def clear_response():
            config.assistant_response = None

        def interrupt_write():
            config.interrupt_flag = True  
        
        window = tk.Tk()
        window.title("Chat") 
        window.geometry("200x330+95+350")
        
        # Dark theme colors
        bg_color = "#2e2e2e"
        fg_color = "#ffffff"
        button_bg = "#404040"
        button_active = "#4d4d4d"
        
        window.configure(bg=bg_color)
        
        button_configs = [
            ("Write scene (Ds)", write_scene1),
            ("Write scene (Qwen)", write_scene2),
            ("Custom Prompt (Ds)", custom_prompt),
            ("Stop Writing", interrupt_write),
            ("Remove Last Response", remove_last),
            ("Insert Response", insert_response), 
            ("Clear Response", clear_response)
        ]
        
        for text, command in button_configs:
            button = tk.Button(
                window,
                text=text,
                command=command, 
                bg=button_bg,
                fg=fg_color,
                activebackground=button_active,
                activeforeground=fg_color,
                relief="flat",
                padx=10
            )
            button.pack(pady=15)
        
        def on_closing():
            window.destroy()
            self.ui_thread = None
            
        window.protocol("WM_DELETE_WINDOW", on_closing)
        window.mainloop()

    def start(self):
        if self.ui_thread is None or not self.ui_thread.is_alive():
            self.ui_thread = threading.Thread(target=self.create_window, daemon=True)
            self.ui_thread.start()
        else:
            print("UI is already running")

# Simulate a long-running task that checks the interrupt flag (for debugging)
    def long_running_task(self):
        import time
        config.interrupt_flag = False
        for i in range(10):  
            if config.interrupt_flag:
                print("Task interrupted!")
                return
            print(f"Working... {i+1}/10")
            time.sleep(1)
        print("Task completed!")

# Create an instance of the UI
Chat_UI = ChatUI()