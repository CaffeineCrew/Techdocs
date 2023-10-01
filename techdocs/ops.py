import argparse
import json
from typing import Dict, List, Optional, Any, Callable

import techdocs
from .dtypes import data_types
from .utils.functools import *
from .utils.parse import *


parser = argparse.ArgumentParser(
        description='Code documentation generation',
        epilog="Thanks for using Techdocs")
subparsers = parser.add_subparsers(help='subcommands')


def depends_login(func: Callable):
    def update_config(cls: Any, config: Dict[str, Any]):
        data = {
            "username":config['username'],
            "password":config['password']
            }

        config.update({"access_token":get_access_token(data)})
        return func(cls, config)
    return update_config


class _SubCommand:
    def __init__(self, name: str, help: str, args_parse: Optional[List[Dict[str, Any]]] = None, pre_compile: bool = False):
        self.name = name
        self.parser = subparsers.add_parser(name, help=help)
        self.parser.set_defaults(subcommand=name)

        self.pre_compile = pre_compile

        if args_parse and pre_compile:
            self.build(args_parse)
        else:
            self.arg_parse = args_parse
    
    def _run(self):
        raise NotImplementedError()
    
    def build(self, args_parse: Optional[List[Dict[str, Any]]] = None):
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
        self._run = func
        self.parser.set_defaults(ops=self._run)




class Ops:
    sub_commands: Dict[str, _SubCommand] = {}
    with open('techdocs/utils/subcommand_signatures.json') as f:
        encoded_sub_commands = json.load(f)


    if encoded_sub_commands['dynamic signatures']:
        sub_commands.update({sub_command['name']: _SubCommand(**sub_command, pre_compile=False) 
                                                        for sub_command in encoded_sub_commands['dynamic signatures']
                                            })

    if encoded_sub_commands['pre-compiled signatures']:
        sub_commands.update({sub_command['name']: _SubCommand(**sub_command, pre_compile=True) 
                                                        for sub_command in encoded_sub_commands['pre-compiled signatures']
                                            })

    @classmethod
    def configure_and_build_subcommand(cls, func):
        config = None
        try:
            args = parser.parse_args()
            sub_command = cls.sub_commands[args.subcommand]
            
            if not sub_command.pre_compile:
                sub_command.build()
            

            sub_command.bind = cls.__getattribute__(cls(), args.subcommand)
            
            func = sub_command.parser.get_default('ops')
            config = {k: v for k, v in vars(args).items() if k not in ['subcommand', 'ops']}

        except AttributeError as e:
            config = True
        
        def run_subcommand(**kwargs):
            return func(config)
        return run_subcommand

    
    @classmethod
    @depends_login
    def generate(cls, config: Dict[str, Any]):
        extract_functions_from_directory(config)
    
    @classmethod
    @depends_login
    def apikey(cls, config: Dict[str, Any]):
        issue_api_key(config)

    @classmethod
    def signup(cls, config: Dict[str, Any]):
        signup(config)
    
    @classmethod
    def version(cls, config: Dict[str, Any]):
        print(f"{techdocs.__version__}")
