. 📂 python-backend
└── 📂 _includes/
│  └── 📂 settings/
│    └── 📂 _instructions/          #custom instructions files
│    ├── 📄 Abbreviations.yaml
│    ├── 📄 Chat Settings.yaml
│    ├── 📄 Endpoints.yaml
│    ├── 📄 Models.yaml
│    ├── 📄 Prompts Structure.yaml
│    ├── 📄 Settings.yaml
│    ├── 📄 Variables.yaml
│  ├── 📄 __init__.py
│  ├── 📄 config.py
│  ├── 📄 dispatcher.py
│  ├── 📄 listener.py
│  └── 📂 app/
│    └── 📂 Chat/
│      ├── 📄 __init__.py
│      ├── 📄 Changer.py
│      ├── 📄 Chatter.py
│      ├── 📄 Generator.py
│      ├── 📄 Helpers.py
│      ├── 📄 Summarizer.py
│    └── 📂 Composers/
│      ├── 📄 ApiComposer.py
│      ├── 📄 PromptComposer.py
│    └── 📂 ConfigManager/
│      ├── 📄 __init__.py
│      ├── 📄 ConfigDataClass.py
│      ├── 📄 chat_config.py
│      ├── 📄 story_config.py
│      ├── 📄 override_config.py
│      ├── 📄 commons.py
│    └── 📂 History/
│      └── 📂 Mixins/
│        ├── 📄 ChangerMixin.py
│        ├── 📄 ParserMixin.py
│        ├── 📄 TrimMixin.py
│      ├── 📄 ChatHistory.py
│      ├── 📄 Story.py
│      ├── 📄 Summary.py
│      ├── 📄 Factory.py
│    └── 📂 Streaming/
│      ├── 📄 Streamer.py
│      ├── 📄 TokenHandler.py
│      ├── 📄 stream.py
│    └── 📂 Utility/
│      ├── 📄 __init__.py
│      ├── 📄 readers.py
│      ├── 📄 writers.py
│      ├── 📄 other_utils.py