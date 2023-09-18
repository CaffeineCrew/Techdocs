import mysql.connector
from mysql.connector import errorcode

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from backend.utils import DBConnection
from backend.core.ConfigEnv import config

from langchain.llms import CTransformers, Clarifai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate 

app = FastAPI(title="Techdocs",
              version="V0.0.1",
              description="API for automatic code documentation generation!"
              )

from backend import router

try:
    dbconnection = DBConnection()
    test_conn = DBConnection.get_client().get_server_info()

    # send prompt wizardcoderLM-70b-instruct-GGUF model
    # with open("backend/utils/prompt.txt",'r') as f:
    #     prompt = f.read()
    # prompt = """You are an AI Coding Assitant and your task is to generate an elaborate, high quality docstring for the query function given by the user. A docstring consists of the following sections:
    #             1. Description: Is the description of what the function does.
    #             2. Arguments: 
    #                 1. Argument Name: Description of the argument and its type.
    #             3. Returns: Description of the return value of the function if any.
    #             4. Raises: Description of the errors that can be raised by the function if any.
    
    #             Instruction: {instruction}
                        
    #             Your task is to generate a docstring for the above query.
    #             Response:
    #         """

    # prompt = PromptTemplate(template=prompt, input_variables=['instruction'])

    # llm = Clarifai(
    #     pat = config.CLARIFAI_PAT,
    #     user_id = config.USER_ID,
    #     app_id = config.APP_ID, 
    #     model_id = config.MODEL_ID,
    #     model_version_id=config.MODEL_VERSION_ID,
    # )

    # llmchain = LLMChain(
    #     prompt=prompt,
    #     llm=llm
    # )

    # app.state.llmchain = llmchain

except mysql.connector.Error as err:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))    


