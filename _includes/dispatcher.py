from .config import config, default_config
from .app.History.Factory import Factory
from .app import ConfigManager
from .app import Chat

def dispatch(folder, file, mode, method, part_number, selected_text):

    if   mode == "story":  return dispatch_story(folder, method, part_number)
    elif mode == "chat":   return dispatch_chat(file, method)
    elif mode == "global": return dispatch_global(method, folder, part_number)
    elif mode == "helper": return dispatch_helper(method, selected_text)

def dispatch_story(folder: str, method: str, part_number: str):

    new_config = ConfigManager.get_story_config(folder, config)
    with ConfigManager.override_config(config, **new_config):
        if method == "write_scene":
            return Chat.Generator.write_scene(part_number)
        elif method == "custom_prompt":     
            return Chat.Generator.custom_prompt(part_number)
        elif method == "regenerate":
            return Chat.Generator.regenerate(part_number)
        elif method == "add_part":
            return Chat.Generator.add_part(part_number)
        elif method == "rewrite_part":
            return Chat.Changer.change_part(part_number)
        elif method == "rewrite_parts":
            return Chat.Changer.change_parts(part_number)
        elif method == "update_summary":
            return Chat.Summarizer.update_summary()
        elif method == "remove_last_response":
            Factory.get_story().remove_last_response()
        else:
            raise Exception(f"Story does not have a {method} method")

def dispatch_chat(file: str, method: str):

    new_config = ConfigManager.get_chat_config(file, config, default_config)
    with ConfigManager.override_config(config, **new_config):
        if method == "chat":
            return Chat.Chatter.chat(file)
        elif method == "remove_last_response":
            Factory.get_chat_history(file).remove_last_response()
        else:
            raise Exception(f"Chat does not have a {method} method")

def dispatch_helper(method: str, selected_text: str):

    if method == "rewrite_selection": 
        return Chat.Helpers.rewrite_selection(selected_text)
    elif method == "translate":
        return Chat.Helpers.translate(selected_text)
    elif method == "explain":
        return Chat.Helpers.explain(selected_text)

def dispatch_global(method: str, folder: str, part_number: int):

    if method == "interrupt_write":      
        config.interrupt_flag = True

    elif method == "switch_debug":
        config.debug = not config.debug
        print(f"Debug mode is {config.debug}") 
    
    elif method == "set_prompt":
        new_config = ConfigManager.get_story_config(folder, config)
        
        prompts = Factory.get_prompts()
        prompt = prompts.get_user_prompt(part_number, new_config['abbreviations'])

        config.variables['#user_prompt'] = prompt