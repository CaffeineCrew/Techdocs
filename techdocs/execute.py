from utils import parse,functools

import argparse

def main():
    parser = argparse.ArgumentParser(description='Weather Application')
    parser.add_argument('--api_key','-k',help='API key for Techdocs')
    parser.add_argument('--username','-u',help='Username for Techdocs')
    parser.add_argument('--password','-p',help='Password for Techdocs')
    parser.add_argument('--dir','-d',help='Root directory to be documented')

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