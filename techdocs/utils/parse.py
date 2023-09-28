import ast
import os
from tqdm import tqdm
import requests

from utils.functools import *


# Function to extract and print the outermost nested function with line number
def extract_outermost_function(node,  config, line_number=1,):
    base_url = "http://localhost:8000"
    if isinstance(node, ast.FunctionDef):
        function_def = ast.unparse(node)
        print(f"Function starting at line {line_number}:\n{function_def}")
        print("=" * 30)

        response = request_inference(config=config,code_block=function_def)
        

    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.FunctionDef):
            line_number = child.lineno
        extract_outermost_function(child, line_number)

# Function to traverse directories recursively and extract functions from Python files
def extract_functions_from_directory(config):
    for root, _, files in os.walk(config["dir"]):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(file_path)
                with open(file_path, "r",errors='ignore') as file:
                    content = file.read()
                parsed = ast.parse(content)
                extract_outermost_function(parsed, config)