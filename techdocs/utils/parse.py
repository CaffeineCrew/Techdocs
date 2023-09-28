import ast
import os
from tqdm import tqdm
import requests

from utils.functools import *


# Function to extract and print the outermost nested function with line number
def extract_outermost_function(node, config):
    
    if isinstance(node, ast.FunctionDef):
        function_def = ast.unparse(node)
        response = request_inference(config=config, code_block=function_def)
        docstr = response['docstr']
        docstring = ast.Expr(value=ast.Str(s=docstr))
        node.body.insert(0, docstring)
        

    for child in ast.iter_child_nodes(node):
        extract_outermost_function(child, config)

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
                docstr_code = ast.unparse(parsed)
                with open(file_path, "w",errors='ignore') as file:
                    file.write(docstr_code)