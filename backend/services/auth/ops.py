from .utils.auth_funcs import *
from .utils.JWTBearer import *
from backend.models import *
from backend.services.db.utils.DBQueries import DBQueries
from backend.core.Exceptions import *
from backend import app

# import openai
# from transformers import RobertaTokenizer, T5ForConditionalGeneration

def ops_signup(response_result: GeneralResponse, data: UserAuth):
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
    
    DBQueries.insert_to_database('auth', (data.username, Auth.get_password_hash(data.password), data.email), 
                                 ['username', 'password', 'email'])
    
    response_result.status = 'success'
    response_result.message = [f'User created successfully']

def ops_login(data:LoginCreds):
    """Wrapper method to handle login process.

    Args:
        data: LoginCreds. User's credentials from the frontend to login to their account.

    Returns:
        TokenSchema. A Pydantic BaseModel to return the JWT tokens to the frontend.

    Raises:
        InvalidCredentialsException: If account with entered credentials does not exist.
    """
    # querying database to check if user already exist
    response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )
    user = DBQueries.fetch_data_from_database('auth', ['username', 'password'], f"username='{data.username}'")
    user = list(user)
    if len(user) == 0:
        # user with the entered credentials does not exist
        raise InvalidCredentialsException(response_result)
    user = user[0]
    if not Auth.verify_password(data.password, user[1]) and Auth.verify_username(data.username, user[0]):
        # password is incorrect
        raise InvalidCredentialsException(response_result)
    
    # password is correct
    return TokenSchema(access_token=Auth.create_access_token(data.username), 
                       refresh_token=Auth.create_refresh_token(data.username),
                       )

def ops_regenerate_api_key(username:str) -> APIKey:

    user_API_entry = DBQueries.fetch_data_from_database('api_key', 'apikey', f"username='{username}'")
    user_API_entry = list(user_API_entry)
    apikey = None

    if len(user_API_entry) != 0:
        apikey = APIKey(api_key=Auth.generate_api_key(username))
        DBQueries.update_data_in_database('api_key','apikey',f"username='{username}'", apikey.api_key)
    
    else:
        apikey = Auth.generate_api_key(username)
        DBQueries.insert_to_database('api_key', (username, apikey), ['username', 'apikey'])
        apikey = APIKey(api_key=apikey)
    
    return apikey
    
        

def ops_inference(source_code:str,api_key:str,username:str):
    response_result = GeneralResponse.get_instance(data={},
                                                   status="not_allowed",
                                                   message=["Not authenticated"]
                                                   )

    user=DBQueries.fetch_data_from_database('api_key', ['apikey'], f"username='{username}'")
    if len(list(user)) == 0:
        # user with the entered credentials does not exist
        raise InfoNotFoundException(response_result,"User not found")
    elif list(user)[0][0]!=api_key:
        raise InvalidCredentialsException(response_result)
    
    def generate_docstring(source_code_message: str):


        llm_response = app.state.llmchain.run({"instruction": source_code_message})

        docstring = Inference(docstr=llm_response)
        
    
        return docstring

    return generate_docstring(source_code)
