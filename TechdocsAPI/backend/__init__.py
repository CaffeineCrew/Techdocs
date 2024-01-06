import mysql.connector

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from backend.utils import DBConnection
from backend.core.ConfigEnv import config

# from langchain.llms import Clarifai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

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
    with open("backend/utils/prompt.txt", "r") as f:
        prompt = f.read()

    prompt = PromptTemplate(template=prompt, input_variables=["instruction"])

    llm = GoogleGenerativeAI(
        model = "gemini-pro",
        google_api_key=config.GOOGLE_API_KEY,
    )

    llmchain = LLMChain(prompt=prompt, llm=llm)
    app.state.llmchain = llmchain

    app.state.templates = Jinja2Templates(directory="./backend/templates")


except mysql.connector.Error as err:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
    )
