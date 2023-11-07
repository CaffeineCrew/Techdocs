import ast
import os
import threading
import time
import glob
from .functools import *
from .LoggingManager import LoggingManager

def extract_outermost_function(node, config):
    """
    This function extracts the docstring of the outermost function in the given AST node.

    Arguments:
    node (ast.Node): The AST node representing the Python code.
    config (dict): A dictionary containing configuration settings.

    Raises:
    IndexError: If the docstring cannot be extracted due to incorrect formatting.

    Note:
    This function inserts the extracted docstring as the first statement in the function body.
    """
    if isinstance(node, ast.FunctionDef):
        function_def = ast.unparse(node)
        response = request_inference(config=config, code_block=function_def)
        if response is not None:
            try:
                docstr = response.split('"""')
                docstring = ast.Expr(value=ast.Str(s=docstr[1]))
                logging_manager = config.get('logging_manager')
                logging_manager.set_log_handlers = [logging_manager.file_handler]
                logging_manager.LOGGER.info(f'Docstring generated for def {node.name}')
                node.body.insert(0, docstring)
            except IndexError:
                pass
    for child in ast.iter_child_nodes(node):
        extract_outermost_function(child, config)

def extract_functions_from_directory(config):
    """
    This function extracts functions from a specified directory.

    Arguments:
    config (dict): A dictionary containing the directory path as the key 'dir'.

    Returns:
    None

    Raises:
    None
    """
    logging_manager = LoggingManager(config['dir'])
    config.update({'logging_manager': logging_manager})
    for root, dirnames, files in os.walk(config['dir']):
        for _file in logging_manager.log_curr_state(root):
            file_path = _file
            with open(file_path, 'r', errors='ignore') as file:
                content = file.read()
            parsed = ast.parse(content)
            extract_outermost_function(parsed, config)
            docstr_code = ast.unparse(parsed)
            write_thread = threading.Thread(target=update_file, args=(file_path, docstr_code))
            write_thread.start()