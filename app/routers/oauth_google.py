from fastapi import APIRouter
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request

from app.models.result import Result
from app.models.user import UserInDB
from app.services.user_service import insert_or_update_user
from app.core import configuration
from app.utils import validate_forwarded_proto
router = APIRouter()

oauth = OAuth()
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
    client_id=configuration.APP_GOOGLE_CLIENT_ID,
    client_secret=configuration.APP_GOOGLE_CLIENT_SECRET,
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_server_side")
    redirect_uri =  validate_forwarded_proto.validateHTTPS(url=redirect_uri, schema=request.headers.get("x-forwarded-proto"))
    print(redirect_uri)
    print (request.headers)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth", response_model=Result)
async def auth_server_side(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    print(token)
    request.session['user'] = dict(user)
    userDB = UserInDB(
        username=user.get("email"),
        email=user.get("email"),
        picture=user.get("picture"),
        given_name=user.get("given_name"),
        family_name=user.get("family_name"),
        disabled=False,
    )
    ret = insert_or_update_user(userDB)
    return Result(code=1, message="Login Success")


@router.get('/logout', response_model=Result)  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)
    return Result(code=1, message="Logout Success")