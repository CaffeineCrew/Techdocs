import mysql.connector
from mysql.connector import errorcode

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from backend.utils import DBConnection
from backend.core.ConfigEnv import config

from langchain.llms import Clarifai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate 

from fastapi_mail import ConnectionConfig, FastMail

app = FastAPI(title="Techdocs",
              version="V0.0.1",
              description="API for automatic code documentation generation!"
              )

from backend import router

try:
    dbconnection = DBConnection()
    test_conn = DBConnection.get_client().get_server_info()

    # send prompt wizardcoderLM-70b-instruct-GGUF model
    with open("backend/utils/prompt.txt",'r') as f:
        prompt = f.read()

    prompt = PromptTemplate(template=prompt, input_variables=['instruction'])

    llm = Clarifai(
        pat = config.CLARIFAI_PAT,
        user_id = config.USER_ID,
        app_id = config.APP_ID, 
        model_id = config.MODEL_ID,
        model_version_id=config.MODEL_VERSION_ID,
    )

    llmchain = LLMChain(
        prompt=prompt,
        llm=llm
    )
    app.state.llmchain = llmchain


    conf = ConnectionConfig(
        MAIL_USERNAME=config.MAIL_USERNAME,
        MAIL_PASSWORD=config.MAIL_PASSWORD,
        MAIL_FROM=config.MAIL_FROM,
        MAIL_PORT=80,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        TEMPLATE_FOLDER="backend/templates",
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
        
        # MAIL_TLS=True,
        # MAIL_SSL=False
    )

    app.state.mail_client = FastMail(conf)
    app.state.templates = Jinja2Templates(directory="./backend/templates")



except mysql.connector.Error as err:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))    


