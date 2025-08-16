from . import config
from .app.Composers.PromptComposer import set_prompt
from .app.History.Factory import Factory
from .app.Utility.ConfigManager import get_story_config, override_config, get_chat_config
from .app import Chat

def dispatch(folder: str, file: str, method: str, chat_mode: bool, part_number: str, selected_text: str):

    result = ""

    if chat_mode: new_config = get_chat_config(file)
    else:         new_config = get_story_config(folder)

    with override_config(config, **new_config):
        
        if method == "write_scene":         
            Chat.Generator.write_scene()
        elif method == "custom_prompt":     
            Chat.Generator.custom_prompt()
        elif method == "rewrite_selection": 
            result = Chat.Helpers.rewrite_selection(selected_text)
        elif method == "translate":         
            result = Chat.Helpers.translate(selected_text)
        elif method == "explain":           
            result = Chat.Helpers.explain(selected_text)
        elif method == "rewrite_part":      
            Chat.Changer.change_part(part_number)
        elif method == "rewrite_parts":     
            Chat.Changer.change_parts(part_number)
        elif method == "regenerate":        
            Chat.Generator.regenerate(part_number)
        elif method == "add_part":          
            Chat.Generator.add_part(part_number)
        elif method == "update_summary":    
            Chat.Summarizer.update_summary()
        elif method == "chat":              
            Chat.Chatter.chat(file)
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