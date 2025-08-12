import os, json, shutil, time
from pathlib import Path

class Utility:

    @staticmethod
    def read_file(file_path):
        path = Path(file_path)
        
        # If the exact file exists, use it
        if path.exists():
            return path.read_text(encoding='utf-8')
        
        # Case-insensitive search
        directory = path.parent if path.parent != Path('.') else Path.cwd()
        target_name = path.name.lower()
        
        for existing_file in directory.iterdir():
            if existing_file.is_file() and existing_file.name.lower() == target_name:
                return existing_file.read_text(encoding='utf-8')
        
        return ""

    @staticmethod
    def write_file(path, content):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with open(path, 'w', encoding='utf-8') as f: 
                    f.write(content)
                break
            except (OSError, IOError) as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff

    @staticmethod
    def print_with_newlines(obj):
        json_str = json.dumps(obj, indent=2, ensure_ascii=False)
        formatted_str = json_str.replace('\\n', '\n')
        print(formatted_str)

    @staticmethod
    def process_tcp_data(data):
        args = data.split(',', 3)
        folder_path, method_name, part_value_str, selected_text = args 

        part_value = int(part_value_str)
        posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')

        return posix_folder_path, method_name, part_value, selected_text

    @staticmethod
    def clear_screen():
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def copy_file(path, new_path):
        if os.path.exists(new_path):
            raise FileExistsError(f"Summary already exists. Please delete it before creating a new one.")
        shutil.copy(path, new_path)