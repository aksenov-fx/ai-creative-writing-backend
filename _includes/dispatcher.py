from _includes import config
from .app.Composers.PromptComposer import set_prompt
from .app.History.Factory import Factory
from .app import ConfigManager
from .app import Chat

def dispatch_story(folder: str, file: str, method: str, part_number: str, selected_text: str):

    result = ""
    new_config = ConfigManager.get_story_config(folder)

    with ConfigManager.override_config(config, **new_config):
        
        if method == "write_scene":         
            return Chat.Generator.write_scene()
        elif method == "custom_prompt":     
            return Chat.Generator.custom_prompt()
        elif method == "rewrite_selection": 
            return Chat.Helpers.rewrite_selection(selected_text)
        elif method == "translate":         
            return Chat.Helpers.translate(selected_text)
        elif method == "explain":           
            return Chat.Helpers.explain(selected_text)
        elif method == "rewrite_part":      
            return Chat.Changer.change_part(part_number)
        elif method == "rewrite_parts":     
            return Chat.Changer.change_parts(part_number)
        elif method == "regenerate":        
            return Chat.Generator.regenerate(part_number)
        elif method == "add_part":          
            return Chat.Generator.add_part(part_number)
        elif method == "update_summary":    
            return Chat.Summarizer.update_summary()
        elif method == "chat":              
            return Chat.Chatter.chat(file)
        elif method == "story_remove_last_response":
            Factory.get_story().remove_last_response()
            return
    
    # No config override
    if method == "interrupt_write":      
        config.interrupt_flag = True

    elif method == "switch_debug":       
        config.debug = not config.debug
        print("Debug mode is on") if config.debug else print("Debug mode is off")
    
    elif method == "set_prompt":
        set_prompt(part_number, new_config['abbreviations'])
    
    else: 
        raise Exception("Story does not have method " + method)

    return result

    
def dispatch_chat(folder: str, file: str, method: str, selected_text: str):

    result = ""
    new_config = ConfigManager.get_chat_config(file)

    with ConfigManager.override_config(config, **new_config):
        
        if method == "chat":              
            return Chat.Chatter.chat(file)
        elif method == "translate":         
            return Chat.Helpers.translate(selected_text)
        elif method == "explain":           
            return Chat.Helpers.explain(selected_text)
        elif method == "chat_remove_last_response":
            Factory.get_chat_history(file).remove_last_response()
    
    # No config override
    if method == "interrupt_write":      
        config.interrupt_flag = True

    elif method == "switch_debug":       
        config.debug = not config.debug
        print("Debug mode is on") if config.debug else print("Debug mode is off")
    
    else: 
        raise Exception("Chat does not have method " + method)

    return result