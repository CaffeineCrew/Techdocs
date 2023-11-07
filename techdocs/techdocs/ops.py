import argparse
import json
from typing import Dict, List, Optional, Any, Callable
import importlib.resources
import techdocs
from .dtypes import data_types
from .utils.functools import *
from .utils.parse import *
parser = argparse.ArgumentParser(description='Code documentation generation', epilog='Thanks for using Techdocs')
parser.add_argument('--version', action='version', version=f'{techdocs.__version__}')
subparsers = parser.add_subparsers(help='subcommands')

def depends_login(func: Callable):
    """
    This decorator function is used to ensure that a user is logged in before executing the decorated function.

    Args:
        func: A function that needs to be executed only if the user is logged in.

    Returns:
        A new function that checks if the user is logged in and updates the configuration with the access token before executing the decorated function.

    Raises:
        Exception: If the user is not logged in, an exception is raised.
    """

    def update_config(cls: Any, config: Dict[str, Any]):
        """
    Updates the configuration for a given class instance.

    Args:
        cls: The class instance for which the configuration is being updated.
        config: A dictionary containing the new configuration settings.

    Returns:
        The updated configuration settings.

    Raises:
        TypeError: If the 'username' or 'password' keys are not present in the
            configuration dictionary.

    This function takes a class instance and a dictionary of configuration
    settings as input. It updates the 'access_token' key in the configuration
    dictionary using the provided 'username' and 'password'. The updated
    configuration dictionary is then returned.
    """
        data = {'username': config['username'], 'password': config['password']}
        config.update({'access_token': get_access_token(data)})
        return func(cls, config)
    return update_config

class _SubCommand:

    def __init__(self, name: str, help: str, args_parse: Optional[List[Dict[str, Any]]]=None, pre_compile: bool=False):
        """
    Initializes the object with the given parameters.

    :param name: The name of the object. (str)
    :param help: A brief description of the object's purpose. (str)
    :param args_parse: A list of dictionaries containing the arguments to be parsed. (Optional[List[Dict[str, Any]]])
    :param pre_compile: Indicates whether the arguments should be compiled beforehand. (bool)

    :raises ValueError: If the input name or help is not a string.
    :raises ValueError: If the input args_parse is not a list of dictionaries.
    :raises ValueError: If the input pre_compile is not a boolean.
    """
        self.name = name
        self.parser = subparsers.add_parser(name, help=help)
        self.parser.set_defaults(subcommand=name)
        self.pre_compile = pre_compile
        if args_parse and pre_compile:
            self.build(args_parse)
        else:
            self.arg_parse = args_parse

    def _run(self):
        """
    This method is not yet implemented.

    Raises:
        NotImplementedError: This error is raised when an attempt is made to call this method.

    Returns:
        None
    """
        raise NotImplementedError()

    def build(self, args_parse: Optional[List[Dict[str, Any]]]=None):
        """
    This method is used to build the argument parser for a command line application.

    Args:
        args_parse: A list of dictionaries containing the arguments to be added to the parser.
            Each dictionary can contain the following keys:
                - args: A list of str representing the argument names.
                - kwargs: A dictionary containing the argument type and any other keyword arguments.
            If None, the method will use the self.arg_parse as the default.

    Returns:
        None

    Raises:
        TypeError: If args_parse is not a list or not an instance of list.
    """
        if not args_parse:
            args_parse = self.arg_parse
        if not isinstance(args_parse, list):
            args_parse = list(args_parse)
        for args_sig in args_parse:
            args_sig['kwargs']['type'] = data_types[args_sig['kwargs']['type']]
            self.parser.add_argument(*args_sig['args'], **args_sig['kwargs'])

    @property
    def bind(self):
        raise PermissionError('Property bind is not allowed to be accessed')

    @bind.setter
    def bind(self, func: Callable):
        """
    Binds a function to the object.

    :param func: The function to be bound.
    :type func: Callable
    :raises TypeError: If the provided argument is not a callable object.

    This method binds a provided function to the object, replacing the default operation.
    It then sets the default operation to the newly bound function.

    """
        self._run = func
        self.parser.set_defaults(ops=self._run)

class Ops:
    sub_commands: Dict[str, _SubCommand] = {}
    with importlib.resources.open_text('techdocs.signatures', 'subcommand_signatures.json') as f:
        encoded_sub_commands = json.load(f)
    if encoded_sub_commands['dynamic signatures']:
        sub_commands.update({sub_command['name']: _SubCommand(**sub_command, pre_compile=False) for sub_command in encoded_sub_commands['dynamic signatures']})
    if encoded_sub_commands['pre-compiled signatures']:
        sub_commands.update({sub_command['name']: _SubCommand(**sub_command, pre_compile=True) for sub_command in encoded_sub_commands['pre-compiled signatures']})

    @classmethod
    def configure_and_build_subcommand(cls, func):
        """
    This class method is responsible for configuring and building a specific subcommand.

    Args:
        func: The function that will be executed within the subcommand.

    Returns:
        A new function that will execute the given function within the specified subcommand.

    Raises:
        AttributeError: If there's an error while trying to access the attributes of the arguments.

    This method first parses the command-line arguments, then retrieves the specified subcommand. If the subcommand does not have a pre-compile step, it will build the subcommand. The method then binds the subcommand to the class attribute that corresponds to the given subcommand name. It also sets the 'ops' default value to the function parser.

    The method then creates a new dictionary with all the command-line arguments that are not 'subcommand' or 'ops'. This dictionary is used to configure the subcommand.

    Finally, the method defines a new function, 'run_subcommand', which takes keyword arguments and executes the given function within the context of the configured subcommand. This new function is then returned.
    """
        config = None
        try:
            args = parser.parse_args()
            sub_command = cls.sub_commands[args.subcommand]
            if not sub_command.pre_compile:
                sub_command.build()
            sub_command.bind = cls.__getattribute__(cls(), args.subcommand)
            func = sub_command.parser.get_default('ops')
            config = {k: v for (k, v) in vars(args).items() if k not in ['subcommand', 'ops']}
        except AttributeError as e:
            config = True

        def run_subcommand(**kwargs):
            """
    Runs a specified subcommand with the given configuration.

    Args:
        **kwargs: A dictionary of keyword arguments containing the configuration
            for the subcommand. The specific keys and their types depend on the
            subcommand being run.

    Returns:
        The result of the subcommand execution. The exact type and structure of
        the return value depend on the subcommand being run.

    Raises:
        Exception: If an error occurs during subcommand execution.
    """
            return func(config)
        return run_subcommand

    @classmethod
    @depends_login
    def generate(cls, config: Dict[str, Any]):
        """
    This method is a class method that is dependent on a login session. It processes a given configuration
    dictionary to extract functions from a specified directory.

    Args:
        cls (type): This is a reference to the current class, used to access class attributes.
        config (Dict[str, Any]): A dictionary containing configuration settings. The dictionary's keys
            should be the names of the functions to extract and the corresponding values should be the
            paths to the directories where these functions are located.

    Raises:
        TypeError: If the input 'config' is not a dictionary.
        ValueError: If the dictionary 'config' contains keys that are not strings or values that are not strings.

    Returns:
        None
    """
        extract_functions_from_directory(config)

    @classmethod
    @depends_login
    def apikey(cls, config: Dict[str, Any]):
        """
    This method generates an API key based on the provided configuration.

    Args:
        config: A dictionary containing the necessary configuration parameters.
            Expected keys: 'user_id', 'user_email', 'client_id', 'client_secret'
            Types: str

    Raises:
        Exception: If any of the required configuration parameters are missing.

    Returns:
        str: The generated API key.
    """
        issue_api_key(config)

    @classmethod
    def signup(cls, config: Dict[str, Any]):
        """
    This method is used to sign up a new user with the provided configuration.

    Args:
        config: A dictionary containing the user's signup information.

    Raises:
        ValueError: If the configuration dictionary is not provided or is empty.

    Returns:
        None
    """
        signup(config)

    @classmethod
    def version(cls, config: Dict[str, Any]):
        """
    This method is a class method that prints the current version of TechDocs.

    Args:
        config: A dictionary containing configuration settings.

    Returns:
        None

    Raises:
        None
    """
        print(f'{techdocs.__version__}')