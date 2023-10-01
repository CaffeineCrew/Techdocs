from .ops import Ops


@Ops.configure_and_build_subcommand
def main(log_info: bool = False):
    if log_info:
        print(
        """

        👋 Hi there! Welcome to techdocs. Here are some cool things you can do:


        💫 try out a demo with or new GUI 🚀 and explore how to use the CLI:

        ➡️     https://techdocs.streamlit.app/

        💫 signup here to get an API key 👤:

        $     techdocs signup -u <username> -p <password> -e <email>

        💫 use the line below to issue a new API key 🗝️:

        $     techdocs apikey -u <username> -p <password>

        💫 use the CLI to generate documentation for your project 📚:

        $     techdocs generate -k <api_key> -u <username> -p <password> -d <directory>

        """
        )
    
    # parser.add_argument('--api_key','-k',type=str,required=True,help='API key for Techdocs')
    
    # parser.add_argument('--username','-u',type=str,required=True,help='Username for Techdocs')

    # parser.add_argument('--password','-p',type=str,required=True,help='Password for Techdocs')

    # parser.add_argument('--dir','-d',type=str,required=True,help='Root directory to be documented')
    
    # # parser.add_argument('--version','-v',action='version',version="%(prog)s 0.0.1")

    # args=parser.parse_args()

    

    # data = {
    #         "username":config['username'],
    #         "password":config['password']
    #         }

    # config.update({"access_token":functools.get_access_token(data)})

    # parse.extract_functions_from_directory(config)
    
if __name__ == '__main__':
    main()