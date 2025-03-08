import tkinter as tk
import threading
from tkinter import ttk

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
            write_thread = threading.Thread(target=Chat.write_scene, args=(config.model,))
            write_thread.start()

        def custom_prompt():
            config.interrupt_flag = False
            write_thread = threading.Thread(target=Chat.custom_prompt, args=(config.model,))
            write_thread.start()
            
        def remove_last():
            ChatHistory.remove_last_response()
            
        def insert_response():
            ChatHistory.insert(config.assistant_response)
            
        def clear_response():
            config.assistant_response = None

        def interrupt_write():
            config.interrupt_flag = True  
        
        def on_model_selected(event):
            selected_model = model_var.get()
            config.model = chat_endpoints.models[selected_model]
        
        window = tk.Tk()
        window.title("Chat") 
        window.geometry("200x320+95+350")
        
        # Dark theme colors
        bg_color = "#2e2e2e"
        fg_color = "#ffffff"
        button_bg = "#404040"
        button_active = "#4d4d4d"
        
        window.configure(bg=bg_color)
        
        button_configs = [
            ("Write scene", write_scene1),
            ("Custom Prompt", custom_prompt),
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
            button.pack(pady=10)
        
        # Model selector - now at the bottom of the window
        model_frame = tk.Frame(window, bg=bg_color)
        model_frame.pack(pady=10, fill=tk.X, padx=10, side=tk.BOTTOM)
        
        model_var = tk.StringVar()
        model_var.set(next(iter(chat_endpoints.models.keys())))  # Default to first model
        
        model_dropdown = ttk.Combobox(model_frame, textvariable=model_var, state="readonly")
        model_dropdown["values"] = list(chat_endpoints.models.keys())
        model_dropdown.pack(fill=tk.X)
        model_dropdown.bind("<<ComboboxSelected>>", on_model_selected)
        
        # Set initial model
        config.model = chat_endpoints.models[model_var.get()]
        
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

# Create an instance of the UI
Chat_UI = ChatUI()