import ssl
from urllib.request import Request, urlopen
import uuid
from app.core import configuration
from app.utils.currentmillis import current
import mimetypes
API_KEY = configuration.APP_GRAFANA_TOKEN
VERIFY_SSL_IMAGE = configuration.APP_VERIFY_SSL_IMAGE
TIME_OUT = configuration.APP_TIME_OUT_DOWNLOAD
def downloadImage(url: str):
    req = Request(url)
    req.add_header('Authorization', 'Bearer {0}'.format(API_KEY))
    if VERIFY_SSL_IMAGE == True:
        r = urlopen(req, timeout=TIME_OUT)
    else:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        r = urlopen(req,context=ctx,timeout=TIME_OUT)
    content_type = r.info().get('Content-Type')
    content = r.read()
    extension = mimetypes.guess_extension(content_type)
    filename = str(uuid.uuid4()) + extension
    return content, content_type, filename, extension



def downloader_file(url: str, header: str = None, header_content: str = None):
    req = Request(url)
    if header is not None:
        req.add_header(header, header_content)
    if VERIFY_SSL_IMAGE == True:
        r = content = urlopen(req, timeout=TIME_OUT)
    else:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        r = urlopen(req,context=ctx,timeout=TIME_OUT)
    content_type = r.info().get('Content-Type')
    content = r.read()
    extension = mimetypes.guess_extension(content_type)
    filename = str(uuid.uuid4()) + extension
    return content, content_type, filename, extension