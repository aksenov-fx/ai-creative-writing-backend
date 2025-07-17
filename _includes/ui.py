import tkinter as tk
import threading
from tkinter import ttk

from _includes import Chat, ChatHistory, config, models

class ChatUI:
    def __init__(self):
        config.interrupt_flag = False
        self.ui_thread = None

    def create_window(self):
        def write_scene():
            config.interrupt_flag = False
            write_thread = threading.Thread(target=Chat.write_scene, args=(config.model,))
            write_thread.start()

        def custom_prompt():
            config.interrupt_flag = False
            write_thread = threading.Thread(target=Chat.custom_prompt, args=(config.model,))
            write_thread.start()
            
        def remove_last():
            ChatHistory.remove_last_response()
            
        def remove_reasoning():
            ChatHistory.remove_reasoning()

        def interrupt_write():
            config.interrupt_flag = True  
        
        def on_model_selected(event):
            selected_model = model_var.get()
            config.model = models[selected_model]
            
        def refine():
            config.interrupt_flag = False
            part_value = int(part_var.get())
            thread = threading.Thread(target=Chat.refine, args=(config.model, part_value))
            thread.start()
            
        def rewrite():
            config.interrupt_flag = False
            part_value = int(part_var.get())
            thread = threading.Thread(target=Chat.rewrite, args=(config.model, part_value))
            thread.start()
            
        def regenerate():
            config.interrupt_flag = False
            part_value = int(part_var.get())
            thread = threading.Thread(target=Chat.regenenerate, args=(config.model, part_value))
            thread.start()
            
        def add_part():
            config.interrupt_flag = False
            part_value = int(part_var.get())
            thread = threading.Thread(target=Chat.add_part, args=(config.model, part_value))
            thread.start()
        
        def summarize():
            config.interrupt_flag = False
            write_thread = threading.Thread(target=Chat.summarize, args=(config.model,))
            write_thread.start()

        def update_summary():
            config.interrupt_flag = False
            write_thread = threading.Thread(target=Chat.update_summary, args=(config.model,))
            write_thread.start()

        window = tk.Tk()
        window.title("Chat") 
        window.geometry("200x550+95+350")
        
        # Dark theme colors
        bg_color = "#2e2e2e"
        fg_color = "#ffffff"
        button_bg = "#404040"
        button_active = "#4d4d4d"
        
        window.configure(bg=bg_color)
        
        # Create a main frame to hold the buttons
        main_frame = tk.Frame(window, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        button_configs = [
            ("Write scene", write_scene),
            ("Custom Prompt", custom_prompt),
            ("Refine", refine),
            ("Rewrite", rewrite),
            ("Regenerate", regenerate),
            ("Summarize Story", summarize),
            ("Update Summary", update_summary),
            ("Add Part", add_part),
            ("Stop Writing", interrupt_write),
            ("Remove Reasoning", remove_reasoning),
            ("Remove Last Response", remove_last)
        ]
        
        for text, command in button_configs:
            button = tk.Button(
                main_frame,
                text=text,
                command=command, 
                bg=button_bg,
                fg=fg_color,
                activebackground=button_active,
                activeforeground=fg_color,
                relief="flat",
                padx=10
            )
            button.pack(pady=5, fill=tk.X)
        
        # Bottom frame for part input and model selector
        bottom_frame = tk.Frame(window, bg=bg_color)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Part input box - first from the bottom
        part_frame = tk.Frame(bottom_frame, bg=bg_color)
        part_frame.pack(fill=tk.X, pady=(0, 10))
        
        part_label = tk.Label(part_frame, text="Part:", bg=bg_color, fg=fg_color)
        part_label.pack(side=tk.LEFT, padx=(0, 5))
        
        part_var = tk.StringVar(value="1")  # Default value is 1
        part_entry = tk.Entry(part_frame, textvariable=part_var, width=5)
        part_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Model selector - last at the bottom
        model_frame = tk.Frame(bottom_frame, bg=bg_color)
        model_frame.pack(fill=tk.X)
        
        model_var = tk.StringVar()
        model_var.set(next(iter(models.keys())))  # Default to first model
        
        model_dropdown = ttk.Combobox(model_frame, textvariable=model_var, state="readonly")
        model_dropdown["values"] = list(models.keys())
        model_dropdown.pack(fill=tk.X)
        model_dropdown.bind("<<ComboboxSelected>>", on_model_selected)
        
        # Set initial model
        config.model = models[model_var.get()]
        
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
Chat_UI.start()