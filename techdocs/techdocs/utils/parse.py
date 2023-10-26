import ast
import os
import threading
import time
import glob

from .functools import *
from .LoggingManager import LoggingManager


# Function to extract and print the outermost nested function with line number
def extract_outermost_function(node, config):
    
    if isinstance(node, ast.FunctionDef):
        function_def = ast.unparse(node)
        response = request_inference(config=config, code_block=function_def)
        if response is not None:
            try:
                docstr = response.split('"""')
                docstring = ast.Expr(value=ast.Str(s=docstr[1]))
                # print(f"Docstring generated for def {node.name}")
                logging_manager = config.get("logging_manager")
                logging_manager.set_log_handlers = [logging_manager.file_handler]
                logging_manager.LOGGER.info(f"Docstring generated for def {node.name}")
                node.body.insert(0, docstring)
            except IndexError:
                pass    
        

    for child in ast.iter_child_nodes(node):
        extract_outermost_function(child, config)

# Function to traverse directories recursively and extract functions from Python files
def extract_functions_from_directory(config):
    logging_manager = LoggingManager(config["dir"])
    config.update({"logging_manager": logging_manager})
    for root, dirnames, files in os.walk(config["dir"]):
        for _file in logging_manager.log_curr_state(root):
            file_path = _file
            with open(file_path, "r",errors='ignore') as file:
                content = file.read()
            parsed = ast.parse(content)
            extract_outermost_function(parsed, config)
            docstr_code = ast.unparse(parsed)
            write_thread = threading.Thread(target=update_file, args=(file_path, docstr_code))
            write_thread.start()