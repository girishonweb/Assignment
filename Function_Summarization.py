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

def find_function_calls(node):
    """Find all function calls inside a function."""
    return [n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]

def summarize_function(node):
    """Summarize the given function node from the AST."""
    summary = {
        'name': node.name,
        'args': [arg.arg for arg in node.args.args],
        'calls': find_function_calls(node),  
        'docstring': ast.get_docstring(node),
        'body': ast.dump(node)
    }
    return summary

def parse_file(file_path):
    """Parse the given Python file and return the AST and summaries of its functions."""
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    
    tree = ast.parse(code)
    function_summaries = {}
    
    # Extract all functions from the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            summary = summarize_function(node)
            print(f"Found function: {summary['name']}")  
            function_summaries[node.name] = summary
    
    return function_summaries, ast.dump(tree)

def resolve_dependencies(function_summaries):
    """Reorder functions based on dependencies."""
    resolved = []
    seen = set()

    def resolve(func_name):
        if func_name not in seen:
            seen.add(func_name)
            if func_name in function_summaries:
                for call in function_summaries[func_name]['calls']:
                    if call in function_summaries:
                        resolve(call)  
                resolved.append(func_name)
            else:
                print(f"Warning: {func_name} not found in function summaries!") 
    for func in function_summaries:
        resolve(func)

    return resolved

def summarize_repo(repo_path):
    """Summarize all functions in the given repository, respecting dependencies."""
    python_files = get_python_files(repo_path)
    repo_summaries = {}
    
    for file_path in python_files:
        file_name = os.path.relpath(file_path, repo_path)
        print(f"Analyzing {file_name}...")  
        function_summaries, ast_representation = parse_file(file_path)
        
        if function_summaries:
            resolved_order = resolve_dependencies(function_summaries)
            ordered_summaries = {func_name: function_summaries[func_name] for func_name in resolved_order}
            
            repo_summaries[file_name] = {
                'functions': ordered_summaries,
                'ast': ast_representation
            }
        else:
            print(f"No functions found in {file_name}.")  
    
    return repo_summaries

# Summarize the repository
summaries = summarize_repo(repo_path)

# Store the result in a JSON file 
with open("repo_function_summaries.json", "w") as json_file:
    json.dump(summaries, json_file, indent=4)

print("Function summarization completed. Results stored in 'repo_function_summaries.json'.")
