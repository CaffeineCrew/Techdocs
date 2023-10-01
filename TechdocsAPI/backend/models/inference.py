from pydantic import BaseModel
from typing import List
from .generic import Base

class Inference(Base):
    docstr:str

class Generate(Base):
    code_block:str
    api_key:str