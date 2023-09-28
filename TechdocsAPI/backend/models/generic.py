from pydantic import BaseModel
from typing import List


class Base(BaseModel):
    @classmethod
    def get_instance(cls, **kwargs):
        return cls(**kwargs)


class GeneralResponse(Base):
    status:str
    message: List[str]
    data:dict