import json
from fastapi import Security
from fastapi.encoders import jsonable_encoder
from fastapi.security.api_key import APIKeyHeader
from starlette.requests import Request
from fastapi.exceptions import HTTPException
from typing import Optional

from app.services.user_service import get_user
from app.models.user import UserInDB
from app.models.token import Token
from app.core import configuration
from app.services import token_service
from app.utils.responses import KEYS_ERROR, get_error_message
from jose import jws
async def get_actual_user(request: Request) -> Optional[dict]:
    user = request.session.get('user')
    if user is not None:
        userDB = get_user(UserInDB(username=user["email"]))
        if userDB is None:
            raise HTTPException(status_code=403, detail='User not Found')
        if userDB.disabled == True:
            raise HTTPException(status_code=403, detail='User Disabled')
        if userDB.admin == False:
            raise HTTPException(status_code=403, detail='You are not admin')
        return userDB
    else:
        raise HTTPException(status_code=403, detail='Could not validate credentials.')
    return None


API_KEY_NAME = configuration.APP_API_KEY_NAME
SECRET = configuration.APP_STATIC_SECRET
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
async def get_api_key(api_key: str = Security(api_key_header)):
    api_key = api_key.replace("Bearer ","",1)
    token = Token(token=api_key, username="")
    ret = token_service.getToken(token)
    if ret is None:
        detail = jsonable_encoder(get_error_message(key=KEYS_ERROR.token_no_valid))
        raise HTTPException(status_code=400, detail=detail)
    else:
        try:
            user = jws.verify(api_key,SECRET,algorithms=['HS256'])
            print(":::::::::::::::::::::::> ", api_key)
            print("-----------------------> ",dict(json.loads(user)))
            return dict(json.loads(user))
        except:
            detail = jsonable_encoder(get_error_message(key=KEYS_ERROR.token_no_valid))
            raise HTTPException(status_code=400, detail=detail)
