from .utils import parse,functools

import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Code documentation generation',
        epilog="Thanks for using Techdocs")
    
    parser.add_argument('--api_key','-k',type=str,required=True,help='API key for Techdocs')
    
    parser.add_argument('--username','-u',type=str,required=True,help='Username for Techdocs')

    parser.add_argument('--password','-p',type=str,required=True,help='Password for Techdocs')

    parser.add_argument('--dir','-d',type=str,required=True,help='Root directory to be documented')
    
    parser.add_argument('--version','-v',action='version',version="%(prog)s 0.0.1")

    args=parser.parse_args()

    config = {
        arg[0]:arg[1] for arg in args._get_kwargs()
    }

    data = {
            "username":config['username'],
            "password":config['password']
            }

    config.update({"access_token":functools.get_access_token(data)})

    parse.extract_functions_from_directory(config)
    
if __name__ == '__main__':
    main()    