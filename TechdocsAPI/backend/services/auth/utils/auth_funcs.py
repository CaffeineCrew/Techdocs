"""Utility class to leverage encryption, verification of entered credentials
and generation of JWT access tokens.
"""
from datetime import datetime, timedelta
from typing import Union, Any
import secrets
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from fastapi.exceptions import HTTPException
from backend.core.ConfigEnv import config
from backend.core.Exceptions import *
from backend.models import TokenPayload, TokenSchema
token_expiry_info = {'ACCESS_TOKEN_EXPIRE_MINUTES': 30, 'REFRESH_TOKEN_EXPIRE_MINUTES': 60 * 24 * 3, 'VERIFICATION_TOKEN_EXPIRE_MINUTES': 20}

class Auth:
    """Utility class to perform -  1.encryption via `bcrypt` scheme.
    2.password hashing 3.verification of credentials and generating
    access tokens.

    Attrs:
        pwd_context: CryptContext. Helper for hashing & verifying passwords
                                   using `bcrypt` algorithm.
    """
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """
    This method is a class method that generates a hashed version of the provided password.

    Args:
        password: The password to be hashed. It should be a string.

    Returns:
        A hashed version of the password. The return type is a string.

    Raises:
        No exceptions are raised by this method.
    """
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
    This method verifies if the provided plain text password matches with the hashed password.

    Args:
        plain_password (str): The plain text password entered by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: Returns True if the plain_password matches with the hashed_password, otherwise False.

    Raises:
        None
    """
        return cls.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def verify_username(entered_username: str, db_username: str) -> bool:
        """
    This function is used to verify if the entered username matches the username stored in the database.

    Arguments:
    entered_username {str} -- The username entered by the user.
    db_username {str} -- The username stored in the database.

    Returns:
    bool -- Returns True if the entered username matches the username stored in the database, False otherwise.
    """
        return entered_username == db_username

    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: int=None, secret_name: str=None) -> str:
        """
@staticmethod
def create_access_token(subject: Union[str, Any], expires_delta: int=None, secret_name: str=None) -> str:
    This function creates an access token using the JWT (JSON Web Token) standard.

    :param subject: The subject of the token. This can be any object that identifies the token's subject.
    :param expires_delta: (Optional) The time delta in which the token will expire. If not provided, the token will expire after 'ACCESS_TOKEN_EXPIRE_MINUTES' minutes.
    :param secret_name: (Optional) The name of the secret key to use for signing the token. If not provided, 'JWT_SECRET_KEY' will be used.
    :raises: If any error occurs while creating the token.
    :returns: The created access token in the form of a string.
"""
        secret_key = config.JWT_SECRET_KEY
        token_expiration = token_expiry_info['ACCESS_TOKEN_EXPIRE_MINUTES']
        if secret_name is not None:
            secret_key = config.dict()['JWT_' + secret_name.upper() + '_SECRET_KEY']
            token_expiration = token_expiry_info[secret_name.upper() + '_TOKEN_EXPIRE_MINUTES']
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=token_expiration)
        to_encode = {'exp': expires_delta, 'sub': str(subject)}
        encoded_jwt = jwt.encode(to_encode, secret_key, config.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def generate_access_tokens_from_refresh_tokens(token: str) -> TokenSchema:
        """Generates a new pair of tokens by implementing rotating
        refresh_access_tokens.

        Args:
            token: str. Current valid refresh access token.

        Returns:
            tokens: TokenSchema. New tokens with new validity.

        Raises:
            LoginFailedException: If the current refresh access token is
                                  invalid.
        """
        tokens = TokenSchema.get_instance(access_token='', refresh_token='')
        try:
            payload = jwt.decode(token, config.JWT_REFRESH_SECRET_KEY, algorithms=[config.ALGORITHM])
            token_data = TokenPayload(**payload)
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(status_code=403, detail='Invalid token or expired token.')
        except (jwt.JWTError, ValidationError):
            raise InvalidCredentialsException(tokens)
        tokens['access_token'] = Auth.create_access_token(token_data.sub)
        tokens['refresh_token'] = Auth.create_access_token(token_data.sub, secret_name='REFRESH')
        return tokens

    @classmethod
    def generate_api_key(cls, username: str):
        """
    This method generates an API key for the given username.

    Args:
        username: The username for which the API key is to be generated.

    Returns:
        A string representing the generated API key.

    Raises:
        TypeError: If the username is not a string.
    """
        return cls.get_password_hash(username + secrets.token_urlsafe(25 - len(username)))

    @classmethod
    def get_user_credentials(cls, access_token: str):
        """
    This method is used to get the user credentials based on the provided access token.

    Args:
        access_token: A string representing the access token.

    Returns:
        The user credentials in the form of a string.

    Raises:
        InvalidCredentialsException: If the access token is invalid or the user is not authenticated.

    """
        response_result = GeneralResponse.get_instance(data={}, status='not_allowed', message=['Not authenticated'])
        try:
            payload = jwt.decode(access_token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM])
            token_data = TokenPayload(**payload)
            return token_data.sub
        except (jwt.JWTError, ValidationError):
            raise InvalidCredentialsException(response_result)

    @classmethod
    def verify_apikey(cls, user_api_key: str, true_api_key: str):
        """
    This method is a class method that verifies the provided API key against the true API key.

    Args:
    user_api_key (str): The API key provided by the user.
    true_api_key (str): The true API key to compare with the user's API key.

    Returns:
    bool: Returns True if the user's API key matches the true API key, and False otherwise.
    """
        return user_api_key == true_api_key