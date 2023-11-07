from pydantic import BaseModel
from typing import List

class Base(BaseModel):

    @classmethod
    def get_instance(cls, **kwargs):
        """
    This is a class method that creates an instance of the class.

    Args:
    **kwargs: Keyword arguments to be passed to the class constructor.

    Returns:
    An instance of the class.

    Raises:
    No exceptions are raised by this method.
    """
        return cls(**kwargs)

class GeneralResponse(Base):
    status: str
    message: List[str]
    data: dict