from fastapi.encoders import jsonable_encoder
from fastapi import status
from starlette.responses import JSONResponse
from app.utils.responses import get_error_message ,get_success_message, KEYS_ERROR, KEYS_SUCCESS

def get_error(key: str = "default", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR ):
    message = jsonable_encoder(get_error_message(key=key))
    return JSONResponse(content=message, status_code=status_code)

def get_success(key: str = "default", status_code: int = status.HTTP_200_OK ):
    message = jsonable_encoder(get_success_message(key=key))
    return JSONResponse(content=message, status_code=status_code)