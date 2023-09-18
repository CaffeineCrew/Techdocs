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

from docguptea.core.ConfigEnv import config
from docguptea.core.Exceptions import *
from docguptea.models import TokenPayload, TokenSchema



ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3 # 3 days


class Auth:
    """Utility class to perform -  1.encryption via `bcrypt` scheme.
    2.password hashing 3.verification of credentials and generating
    access tokens.

    Attrs:
        pwd_context: CryptContext. Helper for hashing & verifying passwords
                                   using `bcrypt` algorithm.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    

    @classmethod
    def get_password_hash(cls,password: str) -> str:
        """Encrypts the entered password.

        Args:
            password: str. Entered password.

        Returns:
            returns hashed(encrypted) password string.
        """
        return cls.pwd_context.hash(password)

    @classmethod    
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Validates if the entered password matches the actual password.

        Args:
            plain_password: str. Entered password by user.
            hashed_password: str. hashed password from the database.

        Returns:
            bool value indicating whether the passwords match or not.
        """
        return cls.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def verify_username(entered_username: str, db_username: str) -> bool:
        """Validates if the entered username matches the actual username.

        Args:
            entered_username: str. Entered `username` by user.
            db_username: str. username from the database.

        Returns:
            bool value indicating whether the village names match or not.
        """
        return entered_username == db_username

    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        """Creates JWT access token.

        Args:
            subject: Union[Any, str]. Hash_key to generate access token from.
            expires_delta: int = None. Expiry time for the JWT.

        Returns:
            encoded_jwt: str. Encoded JWT token from the subject of interest.
        """
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, config.ALGORITHM)
        return encoded_jwt

    @staticmethod    
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        """Creates JWT refresh access token.

        Args:
            subject: Union[Any, str]. Hash_key to generate access token from.
            expires_delta: int = None. Expiry time for the JWT.

        Returns:
            encoded_jwt: str. Encoded JWT token from the subject of interest.
        """
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, config.JWT_REFRESH_SECRET_KEY, config.ALGORITHM)
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
        tokens = TokenSchema.get_instance(
                                        access_token= "",
                                        refresh_token= "",
                                        )
        try:
            payload = jwt.decode(
                token, config.JWT_REFRESH_SECRET_KEY, algorithms=[config.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            if datetime.fromtimestamp(token_data.exp)< datetime.now():
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        except (jwt.JWTError, ValidationError):
            raise InvalidCredentialsException(tokens)
        tokens['access_token'] = Auth.create_access_token(token_data.sub)
        tokens['refresh_token'] = Auth.create_refresh_token(token_data.sub)
        tokens['status'] = 'login successful'
        tokens['role'] = token_data.sub.split("_")[1]
        return tokens

    @classmethod
    def generate_api_key(cls, username: str):
        return cls.get_password_hash(username + secrets.token_urlsafe(25 - len(username)))
    
    @classmethod
    def get_user_credentials(cls,access_token:str):
        response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )
        try:
            payload = jwt.decode(
                access_token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            return token_data.sub
        except (jwt.JWTError, ValidationError):
            raise InvalidCredentialsException(response_result)
        
    @classmethod
    def verify_apikey(cls,user_api_key:str,true_api_key:str):
        return user_api_key == true_api_key

