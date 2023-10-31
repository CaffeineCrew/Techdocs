from fastapi import Request, Depends, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from backend import app
from backend.utils import DBConnection
from backend.models import *
from backend.services.auth import *


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
def api_home():
    return {'detail': 'Welcome to Techdocs API'}

@app.get("/api/response_check", tags=["Resource Server"])
def api_response_check():
    response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )

    try:
        db_msg = ""
        if DBConnection.is_connected():
            db_msg = "Connection Successful to db!"
        else:
            db_msg = "Connection failed to db"

        response_result.message.append(db_msg)

    except Exception as e:
        pass

    return response_result

@app.post("/auth/signup", summary="Creates new user account", response_model=GeneralResponse, tags=["Auth Server"])
async def signup(bgtasks : BackgroundTasks, response: UserAuth):
    response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )
    await ops_signup(bgtasks, response_result, response)

    return response_result

@app.post("/auth/login", summary="Logs in user", response_model=TokenSchema, tags=["Auth Server"])
async def login(response:LoginCreds):
    return ops_login(response)

@app.put("/auth/regenerate_api_key",summary="Forget Password",response_model=APIKey,tags=["Auth Server"],dependencies=[Depends(JWTBearer())])
async def regenerate_api_key(access_token: str = Depends(JWTBearer())):
    user_sub=Auth.get_user_credentials(access_token)

    return ops_regenerate_api_key(user_sub)

@app.post("/api/inference", summary="Inference", response_model=Inference, tags=["Resource Server"], dependencies=[Depends(JWTBearer())])
async def inference(generate: Generate, access_token:str=Depends(JWTBearer())):
    user_sub=Auth.get_user_credentials(access_token)
    
    return ops_inference(generate.code_block,generate.api_key,user_sub)


@app.get("/auth/verify/{token}", summary="Verify Email", response_model=GeneralResponse, tags=["Auth Server"])
async def verify_email(request: Request, token:str):
    response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )

    return ops_verify_email(request, response_result,token)
