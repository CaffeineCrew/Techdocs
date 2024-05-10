import mysql.connector
from mysql.connector import errorcode

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from backend.utils import DBConnection
from backend.core.ConfigEnv import config

from langchain_community.llms import Clarifai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


app = FastAPI(
    title="Techdocs",
    version="V0.0.1",
    description="API for automatic code documentation generation!",
)

from backend import router

try:
    dbconnection = DBConnection()
    test_conn = DBConnection.get_client().get_server_info()

    # send prompt wizardcoderLM-70b-instruct-GGUF model
    with open("backend/utils/Gemini_Prompt.txt", "r") as f:
        prompt = f.read()

    prompt = PromptTemplate(template=prompt, input_variables=["instruction"])

    llm = Clarifai(
        pat=config.CLARIFAI_PAT,
        user_id=config.USER_ID,
        app_id=config.APP_ID,
        model_id=config.MODEL_ID,
        model_version_id=config.MODEL_VERSION_ID,
    )

    llmchain = prompt | llm
    app.state.llmchain = llmchain

    app.state.templates = Jinja2Templates(directory="./backend/templates")


except mysql.connector.Error as err:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
    )
