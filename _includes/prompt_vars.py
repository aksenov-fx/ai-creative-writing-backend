
write = 'Please write a story according to the following guidelines'

# ------------------------------------------- #

guidelines = '''
Make your writing verbose
Fill in the gaps to make smooth transitions between scenes
Employ fresh metaphors drawn from uncommon domains
Describe sensations, thoughts, experiences, associations, smells, tastes, textures, emotions
Include dialogues and direct speech
Maintain a high literary standard of true classic literature
Prioritize originality over convention
Vary sentence structure
Create vivid settings through specific, unexpected details

Avoid cliches and sentimental terms like responsibility, trust, care, accomplishment etc.
Avoid purple prose and florid descriptions
Avoid filler sentences like: "The room held its breath"
Avoid atmospheric descriptions disconnected from character experience, like: "Somewhere, a creek churned with tomorrow’s silt."
'''

# ------------------------------------------- #

user_preprompt = '''
Instructions:
Write the next part of the story based on the below events:
'''

# ------------------------------------------- #

user_postprompt = '''
Stop here
Do not describe any further events after this point
'''

# ------------------------------------------- #

dialogue='''
Instruction
Focus on dialogue in the next scene instead of descriptions
Use direct speech
'''

# ------------------------------------------- #

monolouge='''
Focus on monolouge in the next scene instead of descriptions
Use direct speech and quotations
'''

# ------------------------------------------- #

change_part_preprompt = '''
Change the following story part according to guidelines:
'''

# ------------------------------------------- #

refine_postprompt = '''
Make the above changes only
Preserve the original text when possible
Do not change sentences that do not meet changing requirements
Leave the part heading, if it's present.
Do not return any comments.

Text to change:
'''

# ------------------------------------------- #

rewrite_postprompt = 'Text to change:'

# ------------------------------------------- #

summarize_preprompt = '''
Summarize the following story part as a numbered list of events.
Put each event on a new line.
Keep the part headings
Do not group events by scenes
Include main plot events only
Exclude events that are not relevant to the plot
Do not insert summary introductions or conclusions - just the list of events
'''