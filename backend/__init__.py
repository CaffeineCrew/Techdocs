import mysql.connector
from mysql.connector import errorcode

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from backend.utils import DBConnection

from langchain.llms import CTransformers
from langchain.chains import LLMChain
from langchain import PromptTemplate 

app = FastAPI(title="DocGup-Tea",
              version="V0.0.1",
              description="API for automatic code documentation generation!"
              )

from backend import router

try:
    dbconnection = DBConnection()
    test_conn = DBConnection.get_client().get_server_info()

    # send prompt codellama-13b-instruct-GGUF model
    with open("docguptea/utils/prompt.txt",'r') as f:
        prompt = f.read()
        print(prompt)

    prompt = PromptTemplate(template=prompt,
                            input_variables=['query'])
    
    llm = CTransformers(
        model = "docguptea/static/models/codellama-13b-instruct.Q4_K_M.gguf",
        model_type="llama",
        max_new_tokens = 1096,
        temperature = 0.25,
        repetition_penalty = 1.13,
        stream=True,
        gpu_layers = 10,
    )

    llmchain = LLMChain(
        prompt=prompt,
        llm=llm
    )

    app.state.llmchain = llmchain

except mysql.connector.Error as err:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))    


