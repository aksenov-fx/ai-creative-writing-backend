import json
import hashlib

def calculate_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def print_with_newlines(obj):
    json_str = json.dumps(obj, indent=2, ensure_ascii=False)
    formatted_str = json_str.replace('\\n', '\n')
    print(formatted_str)