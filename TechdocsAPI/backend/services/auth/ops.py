from .utils.auth_funcs import *
from .utils.functools import *
from .utils.JWTBearer import *
from backend.models import *
from backend.services.db.utils.DBQueries import DBQueries
from backend.core.Exceptions import *
from backend.core.ExceptionHandlers import *
from backend.core.ConfigEnv import config
from backend import app
from fastapi import HTTPException, BackgroundTasks
from pydantic import ValidationError
from jose import jwt

async def ops_signup(bgtasks: BackgroundTasks, response_result: GeneralResponse, data: UserAuth):
    """Wrapper method to handle signup process.

    Args:
        response_result: FrontendResponseModel. A TypedDict to return the
                         response captured from the API to the frontend.
        data: UserAuth. New user's prospective credentials from the frontend
                        to create their account.

    Raises:
        ExistingUserException: If account with entered AADHAR Number already exists.
    """

    # querying database to check if user already exist
    user = DBQueries.fetch_data_from_database('auth', ['username', 'email'], f"username='{data.username}' OR email='{data.email}'")
    if len(list(user)) != 0:
        # user with the entered credentials already exists
        raise ExistingUserException(response_result)
    verifiction_token = Auth.create_access_token(f"{data.username} {data.email}", secret_name='VERIFICATION')
    verification_link = f"https://caffeinecrew-techdocs.hf.space/auth/verify/{verifiction_token}"

    email_body_params = {
        'username': data.username, 
        'verify_link': verification_link
    }

    details = {
        "recipients": [data.email],
        "subject": "Welcome to Techdocs:[Account Verification]",
        "template_name": "email_verification.html",
        "template_kwargs": email_body_params
    }
    
    status = post_request(url=config.MAIL_SERVER_URL, data=details, headers=None)
    if status != 200:
        raise EmailNotSentException()


    
    DBQueries.insert_to_database('auth', (data.username, Auth.get_password_hash(data.password), "", 0), 
                                 ['username', 'password', 'email', 'is_verified'])
    
    
    
    response_result.status = 'success'
    response_result.message = [f'Activate your account by clicking on the link sent to {data.email}.\nMake sure to check your spam folder.']

def ops_login(data: LoginCreds):
    """
    Authenticates the user based on provided login credentials.

    Args:
        data: A LoginCreds object containing the username and password for login.

    Returns:
        A TokenSchema object containing the access_token and refresh_token for the authenticated user.

    Raises:
        InvalidCredentialsException: If the provided username or password is incorrect.
        EmailNotVerifiedException: If the user's email is not verified.
    """

    # querying database to check if user already exist
    response_result = GeneralResponse.get_instance(data={}, 
                                                   status='not_allowed', 
                                                   message=['Not authenticated']
                                                )
    user = DBQueries.fetch_data_from_database('auth', ['username', 'password', 'is_verified'], f"username='{data.username}'")
    user = list(user)

    if len(user) == 0:
        # user with the entered credentials does not exist
        raise InvalidCredentialsException(response_result)
    
    user = user[0]
    if not Auth.verify_password(data.password, user[1]) and Auth.verify_username(data.username, user[0]):
        # password is incorrect
        raise InvalidCredentialsException(response_result)
    
    if not user[2]:
        raise EmailNotVerifiedException()
    # password is correct
    return TokenSchema(access_token=Auth.create_access_token(data.username), refresh_token=Auth.create_access_token(data.username, secret_name='REFRESH'))

def ops_regenerate_api_key(username: str) -> APIKey:
    """
    This function is used to regenerate the API key for a given user.

    Args:
        username: A string representing the username of the user for whom the API key needs to be regenerated.

    Returns:
        An instance of the APIKey class, representing the newly generated API key.

    Raises:
        No exceptions are raised by this function.
    """
    user_API_entry = DBQueries.fetch_data_from_database(
        'api_key', 
        'apikey', 
        f"username='{username}'")
    
    user_API_entry = list(user_API_entry)
    apikey = None
    if len(user_API_entry) != 0:
        apikey = APIKey(api_key=Auth.generate_api_key(username))
        DBQueries.update_data_in_database('api_key', 'apikey', f"username='{username}'", apikey.api_key)
    else:
        apikey = Auth.generate_api_key(username)
        DBQueries.insert_to_database('api_key', (username, apikey), ['username', 'apikey'])
        apikey = APIKey(api_key=apikey)
    return apikey

def ops_inference(source_code: str, api_key: str, username: str):
    """
    This function infers the operation from the source code provided.

    Arguments:
    source_code (str): The source code to be analyzed.
    api_key (str): The API key for authentication.
    username (str): The username for authentication.

    Raises:
    InfoNotFoundException: If the user is not found.
    InvalidCredentialsException: If the provided API key does not match the stored API key for the user.

    Returns:
    str: The inferred operation from the source code.
    """
    response_result = GeneralResponse.get_instance(
        data={}, 
        status='not_allowed', 
        message=['Not authenticated'])
    
    user = DBQueries.fetch_data_from_database('api_key', ['apikey'], f"username='{username}'")
    if len(list(user)) == 0:
        raise InfoNotFoundException(response_result, 'User not found')
    elif list(user)[0][0] != api_key:
        raise InvalidCredentialsException(response_result)

    def generate_docstring(source_code_message: str):
        """
    This function generates a docstring for a given Python function based on its source code.

    Arguments:
    source_code_message -- A string containing the source code of a Python function.

    Returns:
    A detailed docstring for the given Python function.

    Raises:
    Exception -- If the source code message is not a string, or if it's not a valid Python function.
    """
        llm_response = app.state.llmchain.run({'instruction': source_code_message})
        docstring = Inference(docstr=llm_response)
        return docstring
    return generate_docstring(source_code)

def ops_verify_email(request: Request, response_result: GeneralResponse, token: str):
    """
    This function verifies the email address provided in the token.

    Args:
        request: The current request object. (type: Request)
        response_result: The response object to hold the result of the operation. (type: GeneralResponse)
        token: The token containing the email address to verify. (type: str)

    Returns:
        A TemplateResponse object containing the appropriate HTML template based on the verification result. (type: app.state.templates.TemplateResponse)

    Raises:
        jwt.JWTError: If there's an error while decoding the JWT token.
        ValidationError: If there's an error while validating the token.
        InfoNotFoundException: If the user associated with the token is not found in the database.

    """
    try:
        payload = jwt.decode(
            token, config.JWT_VERIFICATION_SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            return app.state.templates.TemplateResponse('verification_failure.html', context={'request': request})
        
        username, email = token_data.sub.split(' ', maxsplit=1)
        registered_email = DBQueries.fetch_data_from_database('auth', ['is_verified'], f"username='{username}'")

        registered_email = list(registered_email)
        if len(registered_email) == 0:
            raise InfoNotFoundException(response_result, 'User not found')
        
        # print(registered_email[0][0])
        if registered_email[0][0]:
            return app.state.templates.TemplateResponse("verification_failure.html", context={"request": request})
       
        DBQueries.update_data_in_database('auth','is_verified',f"username='{username}'", (True,))
        DBQueries.update_data_in_database('auth','email',f"username='{username}'", email)
        response_result.status = 'success'
        response_result.message = [f'Email verified successfully']
        return app.state.templates.TemplateResponse('verification_success.html', context={'request': request})
    except (jwt.JWTError, ValidationError):
        return app.state.templates.TemplateResponse('verification_failure.html', context={'request': request})