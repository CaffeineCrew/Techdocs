from .ops import Ops

@Ops.configure_and_build_subcommand
def main(log_info: bool=False):
    """
    This function is the main function of the techdocs application.

    Args:
        log_info: (bool, optional) If True, it prints out a welcome message with some information about the application. Defaults to False.

    Returns:
        None

    Raises:
        None
    """
    if log_info:
        print(
        """

        👋 Hi there! Welcome to techdocs. Here are some cool things you can do:


        💫 try out a demo with our new GUI 🚀 and explore how to use the CLI:

        ➡️     https://techdocs.streamlit.app/

        💫 signup here to get an API key 👤:

        $     techdocs signup -u <username> -p <password> -e <email>

        💫 use the line below to issue a new API key 🗝️:

        $     techdocs apikey -u <username> -p <password>

        💫 use the CLI to generate documentation for your project 📚:

        $     techdocs generate -k <api_key> -u <username> -p <password> -d <directory>

        """
        )
if __name__ == '__main__':
    main()