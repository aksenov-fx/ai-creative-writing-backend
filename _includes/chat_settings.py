from .StoryGenerator.ConfigClass import ChatConfig
from . import prompt_vars as prompt_vars

# --- Chat settings --- #

config = ChatConfig(

    # Prompt vars
        system_prompt=None,
        first_prompt=None,
        user_prompt=None,
        assistant_response=None,

    # Prompt parameters
        model=None,
        temperature=0.8,
        
        # max_tokens for both input and output
        # If input exceeds max_tokens, the first paragraphs will be excluded form input until input matches max_tokens
        max_tokens=100000, 

    # Story path and response separator
        history_path="story.md",
        separator='----',

    # Technical 
        print_messages=True, # Print conversation history in cell outputs
        client_type="openai", # openai or http
        interrupt_flag = False,

    #Reasoning settings
        # Output model reasoning to md file
        # Note: old reasoning will be removed automatically from the request - it does not have to be removed from the file
        # Note: different inference providers output reasoning differently, which may result in <think> tags missing in the output
        # Note: some providers do not allow to define reasoning. These providers can be excluded in openrouter web ui settings
        include_reasoning = True,
        reasoning_header = '### Reasoning', # allows to fold reasoning with code folding
        print_reasoning = False,
        print_output = False,
        part_to_rewrite = 0
)