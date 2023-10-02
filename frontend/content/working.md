1. Navigate into your project directory.

```bash
$ cd <YOUR-PROJECT-DIRECTORY>
```

2. Once the installation is complete, type `techdocs` in the terminal. You should be able to see info about our CLI.

```bash
$ techdocs
```

3. If you are a `new user`, `signup` for a new account using the command below **OR** Head on to [Techdocs](https://techdocs.streamlit.app) and signup for a new account.

```bash
$ techdocs signup -u <username> -p <password> -e <email>
```

4. If you already have your `API KEY`, you can skip step 5.

5. Generate your `API key` using the command below **OR** Head on to [Techdocs](https://techdocs.streamlit.app/demo) and generate your `API KEY`.

```bash
$ techdocs apikey -u <username> -p <password>
```

6. Once you have your `API key`, you can generate the documentation using the command below.

```bash
$ techdocs generate -k <API_KEY> -u <USERNAME> -p <PASSWORD> -d <ROOT-DIRECTORY-OF-THE-PROJECT>
```

6. Wait for the `documentation` to be generated. Your `.py` files will be parsed and the documentation will be generated in the files itself. The tool will log the progress in the terminal and the file will be updated once all the functions are parsed.
