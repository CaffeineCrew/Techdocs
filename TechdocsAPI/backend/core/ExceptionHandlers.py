from backend import app
from .Exceptions import *

from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status



@app.exception_handler(ExistingUserException)
async def handle_existing_user_found(request: Request, exec: ExistingUserException):
    return JSONResponse(status_code=status.HTTP_226_IM_USED,
                        content=repr(exec)
                        )

@app.exception_handler(EmailNotVerifiedException)
async def email_not_verified(request: Request, exec: EmailNotVerifiedException):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                        content=repr(exec)
                        )

@app.exception_handler(InvalidCredentialsException)
async def handle_login_failed(request: Request, exec: InvalidCredentialsException):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                        content=repr(exec)
                        )

@app.exception_handler(InfoNotFoundException)
async def handle_info_not_found(request: Request, exec: InfoNotFoundException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content=repr(exec)
                        )