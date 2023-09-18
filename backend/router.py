from fastapi import Request, Depends, UploadFile
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
        print("Exception :", e)

    return response_result

@app.post("/auth/signup", summary="Creates new user account", response_model=GeneralResponse, tags=["Auth Server"])
async def signup(response: UserAuth):
    response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )
    ops_signup(response_result, response)

    return response_result

@app.post("/auth/login", summary="Logs in user", response_model=TokenSchema, tags=["Auth Server"])
async def login(response:LoginCreds):
    return ops_login(response)

@app.put("/auth/regenerate_api_key",summary="Forget Password",response_model=APIKey,tags=["Auth Server"],dependencies=[Depends(JWTBearer())])
async def regenerate_api_key(access_token: str = Depends(JWTBearer())):
    user_sub=Auth.get_user_credentials(access_token)

    return ops_regenerate_api_key(user_sub)

# @app.post("/api/inference", summary="Inference", response_model=Inference, tags=["Resource Server"], dependencies=[Depends(JWTBearer())])
# async def inference(code_block:str, api_key: str,access_token:str=Depends(JWTBearer())):
#     user_sub=Auth.get_user_credentials(access_token)

#     print("after res")
    
#     return ops_inference(code_block,api_key,user_sub)
