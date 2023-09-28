def add(a, b):
    """
Adds two numbers together.

:param a: The first number to add. Must be a numeric type.
:type a: int or float

:param b: The second number to add. Must be a numeric type.
:type b: int or float

:returns: The sum of the two numbers.
:rtype: int or float

:raises TypeError: If the input parameters are not numeric types.
:raises ValueError: If the input parameters are not numbers.
"""
    return a + b

def multiply(a, b):
    """
Description: 
    This function multiplies two numbers.
    
Arguments: 
    a: First number to be multiplied. It should be an integer or a float.
    b: Second number to be multiplied. It should be an integer or a float.
    
Returns: 
    The product of the two numbers. It will be an integer or a float depending on the input.
    
Raises: 
    None.
"""
    return a * b

def subtract(a, b):
    """
Description: 
    This function performs subtraction of two numbers.
    
Arguments: 
    a (int): The first number to be subtracted.
    b (int): The second number to be subtracted from the first number.
    
Returns: 
    int: Returns the difference of the two numbers.
    
Raises: 
    None
"""
    return a - b

def divide(a, b):
    """
Description:
This function divides two numbers.

Arguments:
a (float): The first number to be divided.
b (float): The second number to be divided.

Returns:
float: Returns the result of a divided by b.

Raises:
ValueError: If b is equal to zero, it raises a ValueError with the message "Cannot divide by zero".
"""
    if b == 0:
        raise ValueError('Cannot divide by zero')
    return a / b

def func(*args, **kwargs):
    """
    This function is a decorator that wraps another function and returns a wrapper function.

    Arguments:
    * args: A variable-length argument list (optional).
    * kwargs: A dictionary of keyword arguments (optional).

    Returns:
    A wrapper function that calls the original function with the same arguments.

    Raises:
    None
    """

    def wrapper(*args, **kwargs):
        """
    This function acts as a wrapper function that calls another function.

    Arguments:
    * args: Positional arguments to be passed to the wrapped function.
             (type: tuple)
    * kwargs: Keyword arguments to be passed to the wrapped function.
              (type: dict)

    Returns:
    The result of calling the wrapped function with the provided arguments.
            (type: any)

    Raises:
    Any exceptions raised by the wrapped function will be propagated.
           (type: any)
    """
        return func(*args, **kwargs)
    return wrapper