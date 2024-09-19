import ast
import os
import json

repo_path = "./AI-voice-assistant"

def get_python_files(directory):
    """Recursively get all Python files from the repository."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files



def find_data_types_in_function(node):
    """Find all data types used in function arguments and variable assignments."""
    data_types = []
    
   
    for arg in node.args.args:
        if isinstance(arg.annotation, ast.Name):
            data_types.append(arg.annotation.id)
    
    
    for n in ast.walk(node):
        if isinstance(n, ast.Assign):
            for target in n.targets:
                if isinstance(n.value, ast.Name):
                    data_types.append(n.value.id)
    
    return data_types

def search_code_for_data_types(repo_path):
    """Search for all instances of data types (int, str, float, etc.) in the repository."""
    python_files = get_python_files(repo_path)
    data_type_usage = {}
    common_data_types = ["int", "str", "float", "list", "dict", "tuple", "set", "bool", "None"]
    
    for file_path in python_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    data_types = find_data_types_in_function(node)
                    if data_types:
                        if file_path not in data_type_usage:
                            data_type_usage[file_path] = []
                        data_type_usage[file_path].append({
                            'function': node.name,
                            'data_types': data_types
                        })
    
    return data_type_usage


data_type_usage = search_code_for_data_types(repo_path)

# Print search results
print("Data types found in repository:")
for file, usage in data_type_usage.items():
    print(f"In file: {file}")
    for entry in usage:
        print(f"  Function: {entry['function']} uses data types: {entry['data_types']}")
