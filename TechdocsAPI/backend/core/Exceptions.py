import json
from backend.models import GeneralResponse, TokenSchema

class InvalidCredentialsException(Exception):

    def __init__(self, token_result: GeneralResponse):
        """
    Initializes an instance of InvalidCredentialsException.

    Arguments:
    token_result -- GeneralResponse: The result of a token request.

    Raises:
    InvalidCredentialsException: If the token request was unsuccessful.

    """
        self.token_result = token_result
        self.set_statuses()
        super(InvalidCredentialsException, self).__init__()

    def set_statuses(self):
        """
    This method updates the status of the token_result attribute to 'login_failed'.

    Arguments:
    self -- The object instance.

    Raises:
    No exceptions are raised by this method.

    Returns:
    None, this method doesn't return a value.
    """
        self.token_result.status = 'login_failed'

    def __repr__(self):
        """
    Returns a string representation of the object.
    
    This method is used to return a string that represents the object. This string can be used to reconstruct the object.
    
    Returns:
    str: A string representation of the object.
    """
        return 'exception.InvalidCredentialsException()'

class ExistingUserException(Exception):

    def __init__(self, response_result: GeneralResponse):
        """
    Initializes an instance of ExistingUserException.
    
    Args:
        response_result: GeneralResponse
            The response result object that contains information about the response.
    
    Raises:
        None

    Returns:
        None
    """
        self.response_result = response_result
        self.set_statuses()
        super(ExistingUserException, self).__init__()

    def set_statuses(self):
        """
    This function sets the status and message of the response_result object.

    Args:
        self: The object of the class.

    Returns:
        None

    Raises:
        None
    """
        self.response_result.status = f'failed'
        self.response_result.message.append(f'user already has an account')
        self.response_result.message[0] = 'authenticated'

    def __repr__(self):
        """
    This method returns a representation of the object.

    Returns:
    exception.ExistingUserException: This exception is raised when a user with the same username already exists.

    Raises:
    No exceptions are raised by this method.

    """
        return 'exception.ExistingUserException()'

class InfoNotFoundException(Exception):

    def __init__(self, response_result: GeneralResponse, message: str):
        """
    Initializes an instance of InfoNotFoundException.
    
    This is a custom exception class used when information is not found.
    
    Args:
    response_result: GeneralResponse
        The response result object.
    message: str
        A human-readable message describing the error.
        
    Raises:
    Exception
        If the initialization fails.
        
    """
        self.response_result = response_result
        self.message = message
        self.set_statuses()
        super(InfoNotFoundException, self).__init__(message)

    def set_statuses(self):
        """
    This method updates the status and message in the response_result dictionary.

    Args:
        self: The object instance.

    Attributes:
        response_result: A dictionary containing the response result.

    Methods:
        self.response_result['status'] = 'abort': Updates the status in the response_result dictionary to 'abort'.
        self.response_result['message'][0] = 'authenticated': Updates the first message in the message list in the response_result dictionary to 'authenticated'.
        self.response_result['message'].append(self.message): Appends the value of self.message to the message list in the response_result dictionary.

    Returns:
        None: This method does not return any value.

    Raises:
        None: This method does not raise any exceptions.
    """
        self.response_result['status'] = 'abort'
        self.response_result['message'][0] = 'authenticated'
        self.response_result['message'].append(self.message)

    def __repr__(self):
        """
    Returns a string representation of the object.

    Returns:
    str: A string representation of the object.
    """
        return 'exception.InfoNotFoundException()'

class EmailNotVerifiedException(Exception):

    def __init__(self):
        """
    Initializes an instance of EmailNotVerifiedException.
    
    This method sets the statuses and initializes the exception with a message.

    Parameters:
    self: The instance of the class.

    Returns:
    None: This method doesn't return anything.

    Raises:
    None: This method doesn't raise any exceptions.
    """
        self.set_statuses()
        super(EmailNotVerifiedException, self).__init__()

    def set_statuses(self):
        """
def set_statuses(self):
    """
        self.status = 'EmailNotVerifiedException'

    def __repr__(self):
        """
    This method returns a representation of the object.

    Returns:
    str: A string representation of the object.
    """
        return 'exception.EmailNotVerifiedException()'


class EmailNotSentException(Exception):
    def __init__(self):
        self.set_statuses()
        super(EmailNotSentException, self).__init__()

    def set_statuses(self):
        self.status = 'EmailNotSentException'

    def __repr__(self):
        return "exception.EmailNotSentException()"
